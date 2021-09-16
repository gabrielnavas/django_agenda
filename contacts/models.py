from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True)
    date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    is_show = models.BooleanField(default=True)
    photo = models.ImageField(blank=True, upload_to='pictures/%Y/%m/%d')

    def __str__(self):
        return self.name
