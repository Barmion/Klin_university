import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestRoutesWorkersNoAdmin:

    def test_list(self, api_client):
        url = reverse('api:workers-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK, (
            'Убедитесь, что неавторизованный пользователь имеет доступ к '
            f'эндпоинту {url}.'
        )

    def test_create(self, api_client):
        url = reverse('api:workers-list')
        response = api_client.post(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, (
            'Убедитесь, что неавторизованный пользователь не имеет доступ к '
            f'эндпоинту {url}.'
        )

    def test_retrive(self, api_client, worker):
        url = reverse('api:workers-detail', kwargs={'pk': worker.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK, (
            'Убедитесь, что неавторизованный пользователь имеет доступ к '
            f'эндпоинту {url}.'
        )

    def test_update(self, api_client, worker, data):
        url = reverse('api:workers-detail', kwargs={'pk': worker.id})
        response = api_client.put(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, (
            'Убедитесь, что неавторизованный пользователь не имеет доступ к '
            f'эндпоинту {url}.'
        )

    def test_delete(self, api_client, worker):
        url = reverse('api:workers-detail', kwargs={'pk': worker.id})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, (
            'Убедитесь, что неавторизованный пользователь не имеет доступ к '
            f'эндпоинту {url}.'
        )

    def test_import(self, api_client):
        url = reverse('api:workers-import-excel')
        response = api_client.post(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, (
            'Убедитесь, что неавторизованный пользователь не имеет доступ к '
            f'эндпоинту {url}.'
        )


@pytest.mark.django_db
class TestRoutesWorkersAdmin:

    def test_list(self, admin_api_client):
        url = reverse('api:workers-list')
        response = admin_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK, (
            'Убедитесь, что админ имеет доступ к эндпоинту {url}.'
        )

    def test_create(self, admin_api_client, data):
        url = reverse('api:workers-list')
        response = admin_api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED, (
            'Убедитесь, что админ не имеет доступ к эндпоинту {url}.'
        )

    def test_retrive(self, admin_api_client, worker):
        url = reverse('api:workers-detail', kwargs={'pk': worker.id})
        response = admin_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK, (
            'Убедитесь, что админ имеет доступ к эндпоинту {url}.'
        )

    def test_update(self, admin_api_client, worker, data):
        url = reverse('api:workers-detail', kwargs={'pk': worker.id})
        response = admin_api_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK, (
            'Убедитесь, что неавторизованный пользователь не имеет доступ к '
            f'эндпоинту {url}.'
        )

    def test_delete(self, admin_api_client, worker):
        url = reverse('api:workers-detail', kwargs={'pk': worker.id})
        response = admin_api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT, (
            'Убедитесь, что неавторизованный пользователь не имеет доступ к '
            f'эндпоинту {url}.'
        )

    def test_import(self, admin_api_client, excel_file):
        url = reverse('api:workers-import-excel')
        response = admin_api_client.post(
            url, {'file': excel_file}, format='multipart'
        )
        assert response.status_code == status.HTTP_201_CREATED, (
            'Убедитесь, что админ имеет доступ к эндпоинту {url}.'
        )
