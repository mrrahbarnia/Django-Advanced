from django.test import TestCase,Client
from django.urls import reverse

from accounts.models import User,Profile
from ...models import Category,Post

from datetime import datetime

class TestView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_obj = User.objects.create_superuser(
            email='test@test.com',password='T13431344'
        )
        self.profile_obj = Profile.objects.create(
            user=self.user_obj,first_name='test-firstname',
            last_name='test-lastname',
            description='test-description'
        )
        self.category_obj = Category.objects.create(name='test')
        self.post_obj = Post.objects.create(
            author=self.profile_obj,
            title='title-test',
            content='test-content',
            category = self.category_obj,
            status = True,
            published_date = datetime.now()
        )
    def test_get_postlist_view_loggedin_successful_response(self):
        self.client.force_login(self.user_obj)
        url = reverse("blog:posts")
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(template_name='post_list.html')
    
    def test_get_postlist_view_annonymous_response(self):
        url = reverse("blog:posts")
        response = self.client.get(url)
        self.assertEqual(response.status_code,302)

    def test_get_detail_view_loggedin_successful_response(self):
        self.client.force_login(self.user_obj)
        url = reverse("blog:detail-post",kwargs={'pk':self.post_obj.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,template_name='blog/post_detail.html')