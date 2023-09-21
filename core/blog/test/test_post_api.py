from django.urls import reverse

from rest_framework.test import APIClient

import pytest

from accounts.models import User

from datetime import datetime

@pytest.fixture
def api_client():
    client = APIClient()
    return client

@pytest.fixture
def user_obj():
    user_obj = User.objects.create_superuser(
            email='test@test.com',password='T13431344'
        )
    return user_obj

@pytest.mark.django_db
class TestPostApi():

    def test_get_postlist_response_200_status(self, api_client):
        url = reverse("blog:api-v1:post-list")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_post_response_401_status(self, api_client):
        url = reverse("blog:api-v1:post-list")
        data = {
            'title':'title-test',
            'content':'test-content',
            'status': True,
            'published_date': datetime.now()
        }
        response = api_client.post(url,data)
        assert response.status_code == 401

    def test_create_post_loggedin_response_201_status(self, api_client, user_obj):
        url = reverse("blog:api-v1:post-list")
        data = {
            'title':'title-test',
            'content':'test-content',
            'status': True,
            'published_date': datetime.now()
        }
        api_client.force_authenticate(user_obj)
        response = api_client.post(url,data)
        assert response.status_code == 201

    def test_create_post_loggedin_invalid_data_response_400_status(self, api_client, user_obj):
        url = reverse("blog:api-v1:post-list")
        data = {
            'status': True,
            'published_date': datetime.now()
        }
        api_client.force_authenticate(user_obj)
        response = api_client.post(url,data)
        assert response.status_code == 400
