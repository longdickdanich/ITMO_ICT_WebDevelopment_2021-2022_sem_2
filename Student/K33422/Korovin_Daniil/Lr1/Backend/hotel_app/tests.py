import json

from django.test import TestCase
from rest_framework import status
from django.urls import reverse

from hotel_app.models import Room, Client, Cleaner


class RoomModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Room.objects.create(name='Lux', number=1, floor=1, cost_of_living=1,
                            room_type=1)

    def test_number_label(self):
        room = Room.objects.get(id=1)
        field_label = room._meta.get_field('number').verbose_name
        self.assertEquals(field_label, 'номер')

    def test_floor_label(self):
        room = Room.objects.get(id=1)
        field_label = room._meta.get_field('floor').verbose_name
        self.assertEquals(field_label, 'этаж')

    def test_cost_of_living_label(self):
        room = Room.objects.get(id=1)
        field_label = room._meta.get_field('cost_of_living').verbose_name
        self.assertEquals(field_label, 'цена заселения')

    def test_room_type_label(self):
        room = Room.objects.get(id=1)
        field_label = room._meta.get_field('room_type').verbose_name
        self.assertEquals(field_label, 'тип комнаты')

    def test_get_room(self):
        url = reverse('room-detail', args=[1])
        # указание на url-адрес, который подвергается тестированию
        data = {"id": 1, "name": 'Lux', "number": 1, "floor": 1, "cost_of_living": 1, "room_type": 1}
        # набор данных с которыми будет производиться сравнение полученных от бэкенда данных
        response = self.client.get(url, format='json')

        # получение данных (data) по указанному url-адресу (url) в формате json (format)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # сравнение статус полученного ответа и стандартного статус кода успешного получения данных
        # Справочно: 200 OK -- успешный запрос от клиента серверу.
        self.assertEqual(response.json(), data)
        # Сравнение данных полученных из ответа сервера (response.json().get('Warriors')) с тестовыми данными (data)

    def test_post_room(self):
        url = reverse('room-list')
        # указание на url-адрес, который подвергается тестированию
        data = {"id": 2, "name": 'Lux', "number": 1, "floor": 1, "cost_of_living": 1, "room_type": 1}
        # набор данных с которыми будет производиться сравнение полученных от бэкенда данных
        response = self.client.post(url, data, format='json')

        # получение данных (data) по указанному url-адресу (url) в формате json (format)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), data)
        # Сравнение данных полученных из ответа сервера (response.json().get('Warriors')) с тестовыми данными (data)

    def test_put_room(self):
        url = reverse('room-detail', args=[1])
        # указание на url-адрес, который подвергается тестированию
        data = {"id": 1, "name": 'Lux', "number": 2, "floor": 1, "cost_of_living": 1, "room_type": 1}
        # набор данных с которыми будет производиться сравнение полученных от бэкенда данных
        response = self.client.put(url, data=data, content_type='application/json')
        # получение данных (data) по указанному url-адресу (url) в формате json (format)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), data)
        # Сравнение данных полученных из ответа сервера (response.json().get('Warriors')) с тестовыми данными (data)


class ClientModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Client.objects.create(full_name="Ivan", pasport="123456", city="Moscow")

    def test_full_name_label(self):
        client = Client.objects.get(id=1)
        field_label = client._meta.get_field('full_name').verbose_name
        self.assertEquals(field_label, 'имя')

    def test_pasport_label(self):
        client = Client.objects.get(id=1)
        field_label = client._meta.get_field('pasport').verbose_name
        self.assertEquals(field_label, 'паспорт')

    def test_city_label(self):
        client = Client.objects.get(id=1)
        field_label = client._meta.get_field('city').verbose_name
        self.assertEquals(field_label, 'город')

    def test_get_client(self):
        url = reverse('client-detail', args=[1])
        # указание на url-адрес, который подвергается тестированию
        data = {"id": 1, "full_name": "Ivan", "pasport": "123456", "city": "Moscow", "rooms": []}
        # набор данных с которыми будет производиться сравнение полученных от бэкенда данных
        response = self.client.get(url, format='json')

        # получение данных (data) по указанному url-адресу (url) в формате json (format)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # сравнение статус полученного ответа и стандартного статус кода успешного получения данных
        # Справочно: 200 OK -- успешный запрос от клиента серверу.
        self.assertEqual(response.json(), data)
        # Сравнение данных полученных из ответа сервера (response.json().get('Warriors')) с тестовыми данными (data)

    def test_post_client(self):
        url = reverse('client-list')
        # указание на url-адрес, который подвергается тестированию
        data = {"id": 2, "full_name": "Ivan", "pasport": "123456", "city": "Moscow", "rooms": []}

        # набор данных с которыми будет производиться сравнение полученных от бэкенда данных
        response = self.client.post(url, data, format='json')

        # получение данных (data) по указанному url-адресу (url) в формате json (format)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), data)
        # Сравнение данных полученных из ответа сервера (response.json().get('Warriors')) с тестовыми данными (data)

    def test_put_client(self):
        url = reverse('client-detail', args=[1])
        # указание на url-адрес, который подвергается тестированию
        data = {"id": 1, "full_name": "Igor", "pasport": "654321", "city": "Moscow", "rooms": []}

        # набор данных с которыми будет производиться сравнение полученных от бэкенда данных
        response = self.client.put(url, data=data, content_type='application/json')
        # получение данных (data) по указанному url-адресу (url) в формате json (format)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), data)
        # Сравнение данных полученных из ответа сервера (response.json().get('Warriors')) с тестовыми данными (data)


class CleanerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Cleaner.objects.create(full_name="Ivan", phone="88005553535", contract_number="123456")

    def test_full_name_label(self):
        cleaner = Cleaner.objects.get(id=1)
        field_label = cleaner._meta.get_field('full_name').verbose_name
        self.assertEquals(field_label, 'ФИО')

    def test_phone_label(self):
        cleaner = Cleaner.objects.get(id=1)
        field_label = cleaner._meta.get_field('phone').verbose_name
        self.assertEquals(field_label, 'Телефон')

    def test_contract_number_label(self):
        cleaner = Cleaner.objects.get(id=1)
        field_label = cleaner._meta.get_field('contract_number').verbose_name
        self.assertEquals(field_label, 'Договор')

    def test_old_phone_label(self):
        cleaner = Cleaner.objects.get(id=1)
        field_label = cleaner._meta.get_field('old_phone').verbose_name
        self.assertEquals(field_label, 'Старый телефон')

    def test_get_cleaner(self):
        url = reverse('cleaner-detail', args=[1])
        # указание на url-адрес, который подвергается тестированию

        data = {"id": 1, "full_name": "Ivan", "phone": "88005553535", "contract_number": "123456",
                "old_phone": ""}
        # набор данных с которыми будет производиться сравнение полученных от бэкенда данных
        response = self.client.get(url, format='json')

        # получение данных (data) по указанному url-адресу (url) в формате json (format)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # сравнение статус полученного ответа и стандартного статус кода успешного получения данных
        # Справочно: 200 OK -- успешный запрос от клиента серверу.
        self.assertEqual(response.json(), data)
        # Сравнение данных полученных из ответа сервера (response.json().get('Warriors')) с тестовыми данными (data)

    def test_post_cleaner(self):
        url = reverse('cleaner-list')
        # указание на url-адрес, который подвергается тестированию
        data = {"id": 2, "full_name": "Igor", "phone": "88125553535", "contract_number": "123456",
                "old_phone": "88125553535"}

        # набор данных с которыми будет производиться сравнение полученных от бэкенда данных
        response = self.client.post(url, data, format='json')

        # получение данных (data) по указанному url-адресу (url) в формате json (format)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), data)
        # Сравнение данных полученных из ответа сервера (response.json().get('Warriors')) с тестовыми данными (data)

    def test_put_cleaner(self):
        url = reverse('cleaner-detail', args=[1])
        # указание на url-адрес, который подвергается тестированию
        data = {"id": 1, "full_name": "Igor", "phone": "88125553535", "contract_number": "123456",
                "old_phone": "88005553535"}
        # набор данных с которыми будет производиться сравнение полученных от бэкенда данных
        response = self.client.put(url, data=data, content_type='application/json')
        # получение данных (data) по указанному url-адресу (url) в формате json (format)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), data)
        # Сравнение данных полученных из ответа сервера (response.json().get('Warriors')) с тестовыми данными (data)
