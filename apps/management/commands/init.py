from django.utils import timezone
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django_seed import Seed
from apps.models import User

class Command(BaseCommand):

    help = "This command creates users"

    def handle(self, *args, **options):
        seeder = Seed.seeder(locale='ko_KR')
        seeder.add_entity(User, 1, {
            'name': 'admin',
            'email': 'admin@abc.com',
            'password': make_password('rewq1234'),
            'is_superuser': True,
            'is_active': True,
            'last_login': timezone.now(),
            'created_at': timezone.now(),
            'updated_at': timezone.now(),
            'deleted_at': None
        })
        seeder.execute()