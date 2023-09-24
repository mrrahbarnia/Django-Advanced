from django.core.management.base import BaseCommand

import random
from faker import Faker
from datetime import datetime

from accounts.models import User, Profile
from ...models import Post, Category

category_list = [
    'Django',
    'Python',
    'Programming',
    'Development',
    'Post'
]


class Command(BaseCommand):
    help = "Inserting data to dummy data"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        user = User.objects.create_user(
            email=self.fake.email(), password='T13431344'
        )
        profile = Profile.objects.get(user=user)
        profile.first_name = self.fake.first_name()
        profile.last_name = self.fake.last_name()
        profile.description = self.fake.paragraph(nb_sentences=5)
        profile.save()

        for category in category_list:
            Category.objects.get_or_create(name=category)
        for _ in range(10):
            Post.objects.create(
                author=profile,
                title=self.fake.paragraph(nb_sentences=1),
                content=self.fake.paragraph(nb_sentences=8),
                category=Category.objects.get(
                    name=random.choice(category_list)
                    ),
                status=random.choice([True, False]),
                published_date=datetime.now()
            )
