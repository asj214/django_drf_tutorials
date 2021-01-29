import random
from faker import Faker

from django.core.management.base import BaseCommand
from django_seed import Seed
from user.models import Membership, User, Shop

class Command(BaseCommand):

    help = "This command creates users"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many users you want to create"
        )

    def handle(self, *args, **options):
        number      = options.get("number")
        fake 	    = Fake()           # 기본언어는 영어로 설정되어 있습니다.
        fake        = Faker(["ko_KR"]) # 한국어로 변경, 근데 몇가지 기능은 사용할 수 없습니다.
        seeder      = Seed.seeder()
        memberships = Membership.objects.all()
        shops       = Shop.objects.all()

        seeder.add_entity(User, number, {
            "name"          : lambda x : fake.name(),
            "age"           : lambda x : random.randint(20, 40),
            "password"      : lambda x : fake.password(),
            "phone_number"  : lambda x : fake.phone_number(),
            "address"       : None,
            "membership"    : lambda x : random.choice(memberships),
            "favorite_shop" : lambda x : random.choice(shops)
        })
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} users created!"))