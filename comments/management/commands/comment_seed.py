import random
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django_seed import Seed
from authentication.models import User
from posts.models import Post
from comments.models import Comment


class Command(BaseCommand):
    help = 'this command hello'
    
    def add_arguments(self, parser):
        parser.add_argument('--times', default=2, type=int,help='how many time show message') 
    
    def handle(self, *args, **options):
        times = options.get('times')

        users = User.objects.all()
        posts = Post.objects.all()
        commentable = ContentType.objects.get(model='post')

        seeder = Seed.seeder('ko_KR')
        seeder.add_entity(Comment, times, {
            'commentable_type': commentable,
            'commentable_id': lambda x: random.choice(posts).id,
            'user': lambda x: random.choice(users),
            'deleted_at': None
        })
        seeder.execute()
