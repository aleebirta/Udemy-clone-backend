# Generated by Django 4.1.5 on 2023-01-15 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_remove_course_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='comments',
            field=models.ManyToManyField(blank=True, to='courses.comment'),
        ),
    ]
