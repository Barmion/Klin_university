import factory
from django.contrib.auth import get_user_model


User = get_user_model()


class PositionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'core.Position'

    name = factory.Faker('job')


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class WorkerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'core.Worker'

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    position = factory.SubFactory(PositionFactory)
    is_active = True
    created_by = factory.SubFactory(UserFactory)
