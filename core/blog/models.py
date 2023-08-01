from django.db import models


# Create your models here.
class Post(models.Model):
    '''
    this is a class to define posts for blog app
    '''
    image = models.ImageField(null=True,blank=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    content = models.TextField()
    counted_views = models.IntegerField(default=0)
    category = models.ForeignKey('Category',on_delete=models.SET_NULL,null=True)
    status = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField()

    def __str__(self):
        return self.title

class Category(models.Model):
    '''
    this is a class to define categories
    '''
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

