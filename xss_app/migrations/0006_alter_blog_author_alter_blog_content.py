# Generated by Django 5.0 on 2024-03-25 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xss_app', '0005_rename_blog_post_text_blog_content_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='author',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=models.CharField(max_length=500),
        ),
    ]