from django.db import models


class NewCategory(models.Model):
    name = models.CharField(max_length=10,unique=True)
    nums = models.IntegerField()
    add_time = models.DateTimeField(auto_now_add=True)

