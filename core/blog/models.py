from django.db import models
from django.utils.text import Truncator

# from django.contrib.auth import get_user_model

# getting User model objects
# User = get_user_model()


# Create your models here.
class Post(models.Model):
    """
    this is a class to define posts for blog app
    """

    image = models.ImageField(null=True, blank=True)
    author = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    content = models.TextField()
    counted_views = models.IntegerField(default=0)
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, null=True
    )
    status = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.title

    def get_snippet(self):
        return Truncator(self.content).words(3)


class Category(models.Model):
    """
    this is a class to define categories
    """

    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
