# Generated by Django 5.0 on 2024-01-07 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('xss_app', '0002_alter_question_pub_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Choice',
        ),
    ]
