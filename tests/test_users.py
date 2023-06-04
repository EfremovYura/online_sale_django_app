import json

from rest_framework.response import Response
from rest_framework.test import APITestCase
from users.models import User


class UsersApiTestCase(APITestCase):

    def create_user(self) -> tuple(User, str):
        """
        Создание пользователя
        """
        password: str = 'qwerty123!'
        user: User = User.objects.create_user(username='test', password=password)
        return user, password

    def test_signup(self):
        url: str = '/users/signup'

        response: Response = self.client.post(url,
                                    {'username': 'test', 'password': 'qwerty123!', 'password_repeat': 'qwerty123!'})

        assert response.status_code == 201

    def test_login(self):
        """
        Проверка успешной аутентификации пользователя
        """
        url: str = '/users/login'
        user, password = self.create_user()

        response: Response = self.client.post(url, {'username': user.username, 'password': password})

        assert response.status_code == 200
        assert response.data.get('username') == user.username

    def test_profile_get(self):
        """
        Проверка получения профиля пользователя
        """
        url: str = '/users/profile'
        user, password = self.create_user()
        self.client.login(username=user, password=password)

        response: Response = self.client.get(url)

        assert response.status_code == 200
        assert response.data.get('id') == user.id

    def test_profile(self):
        """
        Проверка успешного обновления параметров пользователя
        """
        url: str = '/users/profile'
        user, password = self.create_user()
        self.client.login(username=user, password=password)
        first_name: str = 'test'
        last_name: str = 'test'

        response: Response = self.client.put(url, json.dumps({'username': user.username, 'first_name': first_name,
                                                              'last_name': last_name}), content_type='application/json')

        assert response.status_code == 200
        assert User.objects.get(id=user.id).first_name == first_name

    def test_update_password(self):
        """
        Проверка успешного обновления пароля пользователя
        """
        url: str = '/users/update_password'
        user, password = self.create_user()
        self.client.login(username=user, password=password)
        new_password: str = 'qwerty111!'

        response: Response = self.client.put(url, json.dumps({'old_password': password, 'new_password': new_password}),
                                             content_type='application/json')
        logged_in: bool = self.client.login(username=user.username, password=new_password)

        assert response.status_code == 200
        assert logged_in
