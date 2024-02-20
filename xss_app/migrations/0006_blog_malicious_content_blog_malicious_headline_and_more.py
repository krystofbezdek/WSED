# Generated by Django 5.0 on 2024-02-20 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xss_app', '0005_rename_blog_post_text_blog_content_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='malicious_content',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='blog',
            name='malicious_headline',
            field=models.BooleanField(default=False),
        ),
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