# import pytest
from django.test import SimpleTestCase,TestCase
# from rest_framework.test import APIClient
# from accounts.models import User
from django.urls import reverse, resolve
from ..views import (
    PostListView, DetalViewPost ,DeletePostView
)


# @pytest.fixture
# def custom_user():
#     user = User.objects.create_user(
#         email="test@test.com",password="T13431344"
#     )
#     return user

# @pytest.fixture
# def client():
#     client = APIClient()
#     return client

# @pytest.mark.django_db
# class TestUrlApi:
    
#     def test_get_post_list_status_200(self, client):
#         url = reverse("blog:api-v1:post-list")
#         response = client.get(url)
#         assert response.status_code == 200

class TestBlog(SimpleTestCase):

    def test_blog_post_list_resolve(self):
        url = reverse("blog:posts")
        self.assertEquals (resolve(url).func.view_class, PostListView)
    
    def test_blog_post_detail_resolve(self):
        url = reverse("blog:detail-post",kwargs={'pk':1})
        self.assertEquals (resolve(url).func.view_class, DetalViewPost)

    def test_blog_post_delete_resolve(self):
        url = reverse("blog:delete-post",kwargs={'pk':1})
        self.assertEquals (resolve(url).func.view_class, DeletePostView)
