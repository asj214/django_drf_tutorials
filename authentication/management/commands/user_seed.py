from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django_seed import Seed
from authentication.models import User


class Command(BaseCommand):
    help = 'this command hello'
    
    def add_arguments(self, parser):
        parser.add_argument('--times', default=2, type=int,help='how many time show message') 
    
    def handle(self, *args, **options):
        times = options.get('times')
        seeder = Seed.seeder()
        seeder.add_entity(User, times, {
            'name': lambda x: seeder.faker.name(),
            'password': make_password('rewq1234'),
            "is_superuser": False
        })
        seeder.execute()
