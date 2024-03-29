import datetime

from django.db import models
from django.utils import timezone
from django.urls import reverse


# Create your models here.
class Blog(models.Model):
    headline = models.CharField(max_length=200)
    content = models.CharField(max_length=500)
    author = models.CharField(max_length=50)
    pub_date = models.DateTimeField("date published", auto_now_add=True)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def get_absolute_url(self):
        return reverse("xss_app:detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.headline
