from rest_framework import serializers
from ...models import Post

# class PostSerialazer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=250)
#     content = serializers.CharField(max_length=1000)

class PostSerialazer(serializers.ModelSerializer):
    class Meta:
        model = Post
        # fields = "__all__"
        # Best practices
        fields = ['id','author','title','content','status','created_date','published_date']


