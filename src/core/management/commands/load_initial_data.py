from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

from core.models import Position, Worker

User = get_user_model()

fake = Faker('ru_RU')


class Command(BaseCommand):
    help = 'Load initial data for the project'

    def handle(self, *args, **options):

        if Position.objects.count() < 10:
            for _ in range(10):
                Position.objects.get_or_create(name=fake.job())

        user = User.objects.create(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )

        for _ in range(20):
            Worker.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                position=Position.objects.order_by('?').first(),
                created_by=user,
            )
