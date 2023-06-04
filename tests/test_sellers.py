import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase
from django.test import Client

from products.models import Product
from sellers.models import Seller
from users.models import User


product_data: dict = {
    "title": "Test_product",
    "model": "Test_product_model",
    "release_date": "2023-06-04"
}

seller_data: dict = {
    "title": "test seller",
    "seller_type": 1,
    "email": "test@test.test",
    "country": "Россия",
    "city": "Москва",
    "street": "Центральная",
    "house_number": "1C",
    "debt": 0.0,
    "products": []
}

@pytest.mark.django_db
class SellersApiTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin: User = User.objects.create_user(username='admin', password='test', is_staff=True)
        cls.na_admin: User = User.objects.create_user(username='na_admin', password='test', is_staff=True,
                                                      is_active=False)
        cls.user: User = User.objects.create_user(username='user', password='test')

        cls.admin_client: Client = Client()
        cls.na_admin_client: Client = Client()
        cls.user_client: Client = Client()

        cls.admin_client.login(username='admin', password='test')
        cls.na_admin_client.login(username='na_admin', password='test')
        cls.user_client.login(username='user', password='test')

        cls.product1: Product = Product.objects.create(title="Test_product1", model="Test_product_model1",
                                                   release_date="2023-06-04")
        cls.product2: Product = Product.objects.create(title="Test_product2", model="Test_product_model2",
                                                   release_date="2023-06-04")

    @pytest.mark.django_db
    def test_create_sellers(cls):
        """
        Проверка создания продукта
        """
        create_url: str = "/sellers/create"

        response_admin: Response = cls.admin_client.post(create_url, seller_data, content_type="application/json")
        response_na_admin: Response = cls.na_admin_client.post(create_url, seller_data, content_type="application/json")
        response_user: Response = cls.user_client.post(create_url, seller_data, content_type="application/json")

        assert response_admin.status_code == status.HTTP_201_CREATED
        assert response_na_admin.status_code == status.HTTP_403_FORBIDDEN
        assert response_user.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_list_sellers(cls):
        """
        Проверка получения списка продуктов
        """
        list_url: str = "/sellers/list"

        response_admin: Response = cls.admin_client.get(list_url, content_type="application/json")
        response_na_admin: Response = cls.na_admin_client.get(list_url, content_type="application/json")
        response_user: Response = cls.user_client.get(list_url, content_type="application/json")

        list_url_country: str = "/sellers/list?country=Россия"

        response_admin_counry: Response = cls.admin_client.get(list_url_country, content_type="application/json")
        response_na_admin_counry: Response = cls.na_admin_client.get(list_url_country, content_type="application/json")
        response_user_counry: Response = cls.user_client.get(list_url_country, content_type="application/json")

        assert response_admin.status_code == status.HTTP_200_OK
        assert response_na_admin.status_code == status.HTTP_403_FORBIDDEN
        assert response_user.status_code == status.HTTP_403_FORBIDDEN

        assert response_admin_counry.status_code == status.HTTP_200_OK
        assert response_na_admin_counry.status_code == status.HTTP_403_FORBIDDEN
        assert response_user_counry.status_code == status.HTTP_403_FORBIDDEN
    @pytest.mark.django_db
    def test_detail_sellers(cls):
        """
        Проверка детальной информации о продукте
        """
        seller: Seller = Seller.objects.create(title="test seller", seller_type=1, email="test@test.test",
                                               country="Россия", city="Москва", street="Центральная", house_number="1C",
                                               debt=0.0, provider=None)

        detail_url: str = f"/sellers/{seller.id}"

        response_admin: Response = cls.admin_client.get(detail_url, content_type="application/json")
        response_na_admin: Response = cls.na_admin_client.get(detail_url, content_type="application/json")
        response_user: Response = cls.user_client.get(detail_url, content_type="application/json")

        assert response_admin.status_code == status.HTTP_200_OK
        assert response_na_admin.status_code == status.HTTP_403_FORBIDDEN
        assert response_user.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_update_sellers(cls):
        """
        Проверка обновление информации о продукте
        """
        seller: Seller = Seller.objects.create(title="test seller", seller_type=1, email="test@test.test", country="Россия",
                                       city="Москва", street="Центральная", house_number="1C", debt=10.0, provider=None)

        new_title: str = "test seller v2"

        detail_url: str = f"/sellers/{seller.id}"

        seller_data['title'] = new_title

        response_admin: Response = cls.admin_client.put(detail_url, seller_data, content_type="application/json")
        response_na_admin: Response = cls.na_admin_client.put(detail_url, seller_data, content_type="application/json")
        response_user: Response = cls.user_client.put(detail_url, seller_data, content_type="application/json")

        new_debt: float = 123.0
        seller_data['debt'] = new_debt

        response_admin_debt: Response = cls.admin_client.put(detail_url, seller_data, content_type="application/json")


        assert response_admin.status_code == status.HTTP_200_OK
        assert response_admin.data.get('title') == new_title

        assert response_na_admin.status_code == status.HTTP_403_FORBIDDEN
        assert response_user.status_code == status.HTTP_403_FORBIDDEN

        assert response_admin_debt.get('debt') != new_debt

    @pytest.mark.django_db
    def test_delete_sellers(cls):
        """
        Проверка удаления продукта
        """
        seller: Seller = Seller.objects.create(title="test seller", seller_type=1, email="test@test.test",
                                               country="Россия", city="Москва", street="Центральная", house_number="1C",
                                               debt=0.0, provider=None)

        detail_url: str = f"/sellers/{seller.id}"

        response_admin: Response = cls.admin_client.delete(detail_url, content_type="application/json")
        response_na_admin: Response = cls.na_admin_client.delete(detail_url, content_type="application/json")
        response_user: Response = cls.user_client.delete(detail_url, content_type="application/json")

        response_admin_after_delete: Response = cls.admin_client.get(detail_url, content_type="application/json")

        assert response_admin.status_code == status.HTTP_204_NO_CONTENT
        assert response_admin_after_delete.status_code == status.HTTP_404_NOT_FOUND

        assert response_na_admin.status_code == status.HTTP_403_FORBIDDEN
        assert response_user.status_code == status.HTTP_403_FORBIDDEN
