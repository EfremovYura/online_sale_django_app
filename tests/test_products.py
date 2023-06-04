import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase
from django.test import Client

from products.models import Product
from users.models import User


product_data: dict = {
    "title": "Test_product",
    "model": "Test_product_model",
    "release_date": "2023-06-04"
}


@pytest.mark.django_db
class ProductsApiTestCase(APITestCase):
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

    @pytest.mark.django_db
    def test_create_products(cls):
        """
        Проверка создания продукта
        """
        create_url: str = "/products/create"

        response_admin: Response = cls.admin_client.post(create_url, product_data, content_type="application/json")
        response_na_admin: Response = cls.na_admin_client.post(create_url, product_data,
                                                               content_type="application/json")
        response_user: Response = cls.user_client.post(create_url, product_data, content_type="application/json")

        assert response_admin.status_code == status.HTTP_201_CREATED
        assert response_na_admin.status_code == status.HTTP_403_FORBIDDEN
        assert response_user.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_list_products(cls):
        """
        Проверка получения списка продуктов
        """
        list_url: str = "/products/list"

        response_admin: Response = cls.admin_client.get(list_url, content_type="application/json")
        response_na_admin: Response = cls.na_admin_client.get(list_url, content_type="application/json")
        response_user: Response = cls.user_client.get(list_url, content_type="application/json")

        assert response_admin.status_code == status.HTTP_200_OK
        assert response_na_admin.status_code == status.HTTP_403_FORBIDDEN
        assert response_user.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_detail_products(cls):
        """
        Проверка детальной информации о продукте
        """
        product: Product = Product.objects.create(title="Test_product", model="Test_product_model",
                                                  release_date="2023-06-04")

        detail_url: str = f"/products/{product.id}"

        response_admin: Response = cls.admin_client.get(detail_url, content_type="application/json")
        response_na_admin: Response = cls.na_admin_client.get(detail_url, content_type="application/json")
        response_user: Response = cls.user_client.get(detail_url, content_type="application/json")

        assert response_admin.status_code == status.HTTP_200_OK
        assert response_na_admin.status_code == status.HTTP_403_FORBIDDEN
        assert response_user.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_update_products(cls):
        """
        Проверка обновление информации о продукте
        """
        product: Product = Product.objects.create(title="Test_product", model="Test_product_model",
                                                  release_date="2023-06-04")
        new_title: str = "Test_product v2"

        detail_url: str = f"/products/{product.id}"

        product_data['title'] = new_title

        response_admin: Response = cls.admin_client.put(detail_url, product_data, content_type="application/json")
        response_na_admin: Response = cls.na_admin_client.put(detail_url, product_data, content_type="application/json")
        response_user: Response = cls.user_client.put(detail_url, product_data, content_type="application/json")

        assert response_admin.status_code == status.HTTP_200_OK
        assert response_admin.data.get('title') == new_title

        assert response_na_admin.status_code == status.HTTP_403_FORBIDDEN
        assert response_user.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_delete_products(cls):
        """
        Проверка удаления продукта
        """
        product: Product = Product.objects.create(title="Test_product", model="Test_product_model",
                                                  release_date="2023-06-04")

        detail_url: str = f"/products/{product.id}"

        response_admin: Response = cls.admin_client.delete(detail_url, content_type="application/json")
        response_na_admin: Response = cls.na_admin_client.delete(detail_url, content_type="application/json")
        response_user: Response = cls.user_client.delete(detail_url, content_type="application/json")

        response_admin_after_delete: Response = cls.admin_client.get(detail_url, content_type="application/json")

        assert response_admin.status_code == status.HTTP_204_NO_CONTENT
        assert response_admin_after_delete.status_code == status.HTTP_404_NOT_FOUND

        assert response_na_admin.status_code == status.HTTP_403_FORBIDDEN
        assert response_user.status_code == status.HTTP_403_FORBIDDEN
