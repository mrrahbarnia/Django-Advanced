from django.test import TestCase

from datetime import datetime

from ...models import Category
from ...forms import PostForm


class TestForm(TestCase):
    
    def test_post_form_with_valid_data(self):
        category_obj = Category.objects.create(name="test")
        form = PostForm(data={
            'title':'test-title',
            'content':'test-content',
            'status':True,
            'category':category_obj,
            'published_date':datetime.now()
        })
        self.assertTrue(form.is_valid())

    def test_post_form_with_invalid_data(self):
        form = PostForm(data={
            'title':'test-title',
        })
        self.assertFalse(form.is_valid())