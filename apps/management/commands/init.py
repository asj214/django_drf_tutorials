from django.utils import timezone
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django_seed import Seed
from apps.models import User, Category


resources = [
    {
        "id": 1,
        "parent": None,
        "name": "상의",
        "is_active": True
    },
    {
        "id": 2,
        "parent": None,
        "name": "아우터",
        "is_active": True
    },
    {
        "id": 3,
        "parent": None,
        "name": "바지",
        "is_active": True
    },
    {
        "id": 4,
        "parent": 1,
        "name": "반팔 티셔츠",
        "is_active": True
    },
    {
        "id": 5,
        "parent": 1,
        "name": "긴팔 티셔츠",
        "is_active": True
    },
    {
        "id": 6,
        "parent": 1,
        "name": "맨투맨/스웨트셔츠",
        "is_active": True
    },
    {
        "id": 7,
        "parent": 1,
        "name": "셔츠 블라우스",
        "is_active": True
    },
    {
        "id": 8,
        "parent": 2,
        "name": "롱 패딩",
        "is_active": True
    },
    {
        "id": 9,
        "parent": 2,
        "name": "숏 패딩",
        "is_active": True
    },
    {
        "id": 10,
        "parent": 2,
        "name": "겨울 기타 코트",
        "is_active": True
    }
]


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

        for row in resources:

            parent = None if row['parent'] is None else Category.objects.get(pk=row['parent'])
            depth = 1 if parent is None else parent.depth + 1

            Category.objects.create(
                id=row['id'],
                parent=parent,
                name=row['name'],
                depth=depth,
                is_active=row['is_active']
            )

        seeder.execute()
