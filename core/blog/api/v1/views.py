from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from ...models import Post
from .serializers import PostSerialazer
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404
from rest_framework import status
# from rest_framework.decorators import api_view,permission_classes

"""
@api_view(['GET','POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_list_view(request):
    if request.method == 'GET':
        posts = Post.objects.filter(status=True)
        serializer = PostSerialazer(posts,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PostSerialazer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
"""

class PostListApiView(ListCreateAPIView):
    """Getting a list of posts and creating new posts"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerialazer
    queryset = Post.objects.filter(status=True)

"""
@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_detail_view(request,id):
    # try:
    #     post = Post.objects.get(pk=id)
    #     serializer = PostSerialazer(post)
    #     return Response(serializer.data)
    # except Post.DoesNotExist:
    #     return Response({"detail":"post does not exist"},status = status.HTTP_404_NOT_FOUND)
    post = get_object_or_404(Post,pk=id,status=True)
    if request.method == 'GET':
        serializer = PostSerialazer(post)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PostSerialazer(post,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(request.data)
    elif request.method == 'DELETE':
        post.delete()
        return Response({"detail":"item deleted successfully"},status=status.HTTP_204_NO_CONTENT)
"""

class PostSingleApiView(RetrieveUpdateDestroyAPIView):
    """Getting a single post by it's id plus eitting and removing it"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerialazer
    queryset = Post.objects.filter(status=True)
    

        