import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from authentication.models import User
from posts.models import Post


class Command(BaseCommand):
    help = 'this command hello'
    
    def add_arguments(self, parser):
        parser.add_argument('--times', default=2, type=int,help='how many time show message') 
    
    def handle(self, *args, **options):
        times = options.get('times')

        users = User.objects.all()

        seeder = Seed.seeder('ko_KR')
        seeder.add_entity(Post, times, {
            'user': lambda x: random.choice(users),
            'deleted_at': None
        })
        seeder.execute()
