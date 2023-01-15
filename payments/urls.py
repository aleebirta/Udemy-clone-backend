
from payments.views import PaymentHandler, WebHook
from django.urls import path

app_name='payments'

urlpatterns = [
    path('webhook/',WebHook.as_view()),
    path('',PaymentHandler.as_view()),
]
