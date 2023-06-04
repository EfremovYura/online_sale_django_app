import factory
from pytest_factoryboy import register
from products.models import Product
from users.models import User


@register
class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker("user_name")
    password = factory.Faker("password")

    class Meta:
        model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return User.objects.create_user(*args, **kwargs)


@register
class ProductFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('sentence')
    model = factory.Faker('sentence')
    release_date = "2023-06-04"

    class Meta:
        model = Product
