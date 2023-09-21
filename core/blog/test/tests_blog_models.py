from django.test import TestCase

from datetime import datetime

from accounts.models import User,Profile
from ..models import Post,Category

class TestModel(TestCase):

    def setUp(self):
        self.user_obj = User.objects.create_user(
            email='test@test.com',password='T13431344')
        self.profile_obj = Profile.objects.create(
            user=self.user_obj,first_name='test-firstname',
            last_name='test-lastname',
            description='test-description'
        )
        self.category_obj = Category.objects.create(name='test')

    def test_create_post_instance_with_valid_data(self):
        post_obj = Post.objects.create(
            author = self.profile_obj,
            title = 'test-title',
            content = 'test-content',
            category = self.category_obj,
            status = True,
            published_date = datetime.now()
        )
        self.assertTrue(Post.objects.filter(pk=post_obj.id).exists())
        self.assertEqual(post_obj.title,'test-title')