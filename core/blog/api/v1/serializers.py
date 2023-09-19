from rest_framework import serializers
from ...models import Post, Category
from accounts.models import Profile


# class PostSerialazer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=250)
#     content = serializers.CharField(max_length=1000)
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class PostSerialazer(serializers.ModelSerializer):
    snippet = serializers.ReadOnlyField(source="get_snippet")
    api_absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        # fields = "__all__"
        # Best practices
        fields = [
            "id",
            "author",
            "title",
            "content",
            "snippet",
            "status",
            "category",
            "api_absolute_url",
            "created_date",
            "published_date",
        ]
        read_only_fields = ["author"]

    def get_api_absolute_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.id)

    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("snippet", None)
            rep.pop("api_absolute_url", None)
        else:
            rep.pop("content", None)
        rep["category"] = CategorySerializer(
            instance.category, context={"request": request}
        ).data
        return rep

    def create(self, validated_data):
        validated_data["author"] = Profile.objects.get(
            user__id=self.context.get("request").user.id
        )
        return super().create(validated_data)
