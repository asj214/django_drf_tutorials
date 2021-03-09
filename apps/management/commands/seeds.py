import random
from faker import Faker
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django_seed import Seed
from apps.models import User, Post


class Command(BaseCommand):

    help = "This command creates users"

    def handle(self, *args, **options):

        # 한국어로 변경, 근데 몇가지 기능은 사용할 수 없습니다.
        fake = Faker(['ko_KR'])
        seeder = Seed.seeder()

        seeder.add_entity(User, 50, {
            'name': lambda x : fake.name(),
            'email': lambda x : fake.email(),
            'password': make_password('rewq1234'),
            'is_superuser': False,
            'is_active': True,
            'last_login': timezone.now(),
            'created_at': timezone.now(),
            'updated_at': timezone.now(),
            'deleted_at': None
        })

        users = User.objects.all()
        seeder.add_entity(Post, 50, {
            'user': lambda x: random.choice(users),
            'title': lambda x : fake.sentence(),
            'body': lambda x : fake.text(),
            'deleted_at': None
        })

        seeder.execute()
