from django.forms import ModelForm
from blog.models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "status", "category", "published_date"]
