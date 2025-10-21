import pytest
from django.urls import reverse
from rest_framework.pagination import PageNumberPagination


@pytest.mark.django_db
class TestContent:

    def test_pagination(self, api_client, workers):
        page_size = PageNumberPagination().page_size
        workers_count = page_size + 1
        workers(workers_count)
        url = reverse('api:workers-list')
        response = api_client.get(url)
        response_data = response.json()

        assert len(response_data['results']) == page_size, (
            'Убедитесь, что в проекте настроена пагинация'
        )

    def test_list_fields(self, api_client, worker):
        required_fields = {
            'id',
            'last_name',
            'first_name',
            'middle_name',
            'position',
            'is_active',
        }
        url = reverse('api:workers-list')
        response = api_client.get(url)
        response_data = response.json()
        response_serializer_fields = set(response_data['results'][0].keys())
        assert response_serializer_fields == required_fields, (
            'Убедитесь, что ответ содержит только базовые поля '
            f'{required_fields}'
        )

    def test_retrive_fields(self, api_client, worker):
        required_fields = {
            'id',
            'last_name',
            'first_name',
            'middle_name',
            'email',
            'position',
            'is_active',
            'created_by',
            'hired_date',
        }
        url = reverse('api:workers-detail', kwargs={'pk': worker.id})
        response = api_client.get(url)
        response_data = response.json()
        response_serializer_fields = set(response_data.keys())
        assert response_serializer_fields == required_fields, (
            'Убедитесь, что ответ содержит все необходимые поля '
            f'{required_fields}'
        )

    def test_filtration(self, api_client, workers):
        workers_count = 10
        workers(workers_count)
        url = reverse('api:workers-list')
        response = api_client.get(url, {'is_active': 'false'})
        response_data = response.json()

        assert len(response_data['results']) == 0, (
            'Убедитесь, что в проекте настроена фильтрация'
        )
