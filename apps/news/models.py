from django.db import models


class NewsCategory(models.Model):
    name = models.CharField(max_length=100)
    nums = models.IntegerField(null=True)
    add_time = models.DateTimeField(auto_now_add=True, null=True)


class News(models.Model):
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    thumbnail = models.URLField()
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('news.NewsCategory', on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey('ozauth.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["-pub_time"]


class Comment(models.Model):
    content = models.CharField(max_length=200)
    pub_time = models.DateTimeField(auto_now_add=True)
    new = models.ForeignKey(News, on_delete=models.CASCADE)
    author = models.ForeignKey('ozauth.User', on_delete=models.CASCADE)

    class Meta:
        ordering = ["-pub_time"]
