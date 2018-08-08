from django.db import models


class NewCategory(models.Model):
    name = models.CharField(max_length=10, unique=True)
    nums = models.IntegerField()
    add_time = models.DateTimeField(auto_now_add=True)


class Banner(models.Model):
    banner_url = models.CharField(max_length=200)
    position = models.IntegerField()
    link_url = models.CharField(max_length=200)
    is_del = models.BooleanField(default=0)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['position']

