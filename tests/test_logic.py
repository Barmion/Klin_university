import pytest
from django.apps import apps
from django.urls import reverse


@pytest.mark.django_db
class TestLogicWorkersNoAdmin:

    def test_cant_create(self, api_client, data):
        Worker = apps.get_model('core', 'Worker')
        url = reverse('api:workers-list')
        response = api_client.post(url, data)
        assert Worker.objects.count() == 0, (
            'Убедитесь, что неавторизованный пользователь '
            'не может создавать записи в базе данных'
        )

    def test_cant_update(self, api_client, worker, data):
        Worker = apps.get_model('core', 'Worker')
        url = reverse('api:workers-detail', kwargs={'pk': worker.id})
        response = api_client.put(url, data)
        updated_worker = Worker.objects.get(id=worker.id)

        assert updated_worker == worker, (
            'Убедитесь, что неавторизованный пользователь '
            'не может изменять записи в базе данных '
        )

    def test_cant_delete(self, api_client, worker):
        Worker = apps.get_model('core', 'Worker')
        url = reverse('api:workers-detail', kwargs={'pk': worker.id})
        response = api_client.delete(url)
        assert Worker.objects.count() == 1, (
            'Убедитесь, что неавторизованный пользователь '
            'не может удалять записи в базе данных'
        )

    def test_cant_import(self, api_client):
        Worker = apps.get_model('core', 'Worker')
        url = reverse('api:workers-import-excel')
        response = api_client.post(url)
        assert Worker.objects.count() == 0, (
            'Убедитесь, что неавторизованный пользователь '
            'не может добавлять записи в базу данных'
            'через импорт'
        )


@pytest.mark.django_db
class TestRoutesWorkersAdmin:

    def test_can_create(self, admin_api_client, data):
        Worker = apps.get_model('core', 'Worker')
        url = reverse('api:workers-list')
        response = admin_api_client.post(url, data)
        assert Worker.objects.count() == 1, (
            'Убедитесь, что админ может создавать записи в базе данных'
        )

    def test_can_update(self, admin_api_client, worker, data):
        Worker = apps.get_model('core', 'Worker')
        url = reverse('api:workers-detail', kwargs={'pk': worker.id})
        response = admin_api_client.put(url, data)
        updated_worker = Worker.objects.get(id=worker.id)

        assert {
            'first_name': updated_worker.first_name,
            'last_name': updated_worker.last_name,
            'email': updated_worker.email,
            'position': updated_worker.position.name
        } == data, (
            'Убедитесь, что админ может изменять записи в базе данных '
        )

    def test_can_delete(self, admin_api_client, worker):
        Worker = apps.get_model('core', 'Worker')
        url = reverse('api:workers-detail', kwargs={'pk': worker.id})
        response = admin_api_client.delete(url)
        assert Worker.objects.count() == 0, (
            'Убедитесь, что админ может удалять записи в базе данных'
        )

    def test_can_import(self, admin_api_client, excel_file):
        Worker = apps.get_model('core', 'Worker')
        url = reverse('api:workers-import-excel')
        response = admin_api_client.post(
            url, {'file': excel_file}, format='multipart'
        )
        assert Worker.objects.count() == 1, (
            'Убедитесь, что админ может добавлять записи в базу данных'
            'через импорт'
        )
