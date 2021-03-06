from django.utils import timezone
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django_seed import Seed
from apps.models import User, Category

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

        resources = [
            {
                'id': 1,
                'parent_id': None,
                'name': '의류',
                'order': 1,
                'depth': 1,
                'is_active': True
            },
            {
                'id': 2,
                'parent_id': 1,
                'name': '신발',
                'order': 1,
                'depth': 2,
                'is_active': True
            },
            {
                'id': 3,
                'parent_id': 1,
                'name': '전자기기',
                'order': 2,
                'depth': 1,
                'is_active': True
            },
            {
                'id': 4,
                'parent_id': 3,
                'name': '스마트폰',
                'order': 1,
                'depth': 2,
                'is_active': True
            },
            {
                'id': 5,
                'parent_id': 3,
                'name': '스마트 워치',
                'order': 2,
                'depth': 2,
                'is_active': True
            },
        ]

        user = User.objects.get(pk=1)

        categories = []
        for r in resources:
            category = Category()
            category.id = r['id']
            category.user = user
            category.parent_id = r['parent_id']
            category.name = r['name']
            category.order = r['order']
            category.depth = r['depth']
            category.is_active = r['is_active']
            categories.append(category)

        Category.objects.bulk_create(categories)