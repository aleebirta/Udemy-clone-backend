from decimal import Decimal

from django.shortcuts import render
import os
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import json
import stripe

from courses.models import Course
from payments.models import PaymentIntent, Payment
from userextend.models import User

# Create your views here.


stripe_api_key = 'sk_test_51MQTAWJ0QiNaJPVnXhENKZ45Hm76QlRHd0OyfaV7WzpAVH1aCRy2rKLADhsAkZ1ZLACj9k4FEW4E2oUJQcR46t3v00AE8IwuMT'
endpoint_secret = ' whsec_9d8c2130c3913fd73799d19a53e04dd2a10349e51a05abb2f7034970808998d8'

stripe.api_key = stripe_api_key


class PaymentHandler(APIView):
    def post(self, request):
        if request.body:
            body = json.load(request.body)
            if body and len(body):
                course_line_items = []
                cart_course = []
                for item in body:
                    try:
                        course = Course.objects.get(course_uuid=item)
                        line_item = {
                            'price_data': {
                                'currency': 'usd',
                                'unit_amount': int(course.price * 100),
                                'product_data': {

                                    'name': course.title
                                },
                            },

                            'quantity': 1
                        }

                        course_line_items.append(line_item)
                        cart_course.append(course)
                    except Course.DoesNotExist:
                        return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        checkout_session = stripe.checkout.Session.Create(
            paymen_method=['card'],
            line_items=course_line_items,
            mode='payment',
            succes_url='http:localhost:3000/',
            cancel_url='http:localhost:3000/',
        )
        intent = PaymentIntent.objects.create(
            payment_intent_id=checkout_session.payment_intent,
            checkout_id=checkout_session.id,
            user=User.objects.get(id=1)
        )
        intent.couse.add(*cart_course)

        return Response({'url': checkout_session.url})


class WebHook(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        even = None
        try:
            event = stripe.Webhook.construct_event(
                payload=payload, sig_header=sig_header )
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']

            try:
                intent = PaymentIntent.objects.get(checkout_id=session.id, payment_intent_id=session.payment_intent)

            except PaymentIntent.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            Payment.objects.create(
                payment_intent=intent,
                total_amount=Decimal(session.amount_total / 100)
            )
            intent.user.paid_courses.add(*intent.course.all())

            return Response(status=200)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)