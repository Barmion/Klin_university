import pytest
from django.apps import apps
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_validate_import(admin_api_client, bad_excel_file):
    url = reverse('api:workers-import-excel')
    response = admin_api_client.post(
        url, {'file': bad_excel_file}, format='multipart'
    )
    bad_fields = response.json()['Записи с ошибками'][0][1].keys()
    assert response.status_code == status.HTTP_400_BAD_REQUEST, (
        'Убедитесь, что если не добавлено ни одной записи, '
        'возвращается ответ 400'
    )
    assert response.json()['Ошибок валидации'] == 1, (
        'Убедитесь, что возвращается верное количество записей '
        'с проблемами валидации'
    )
    assert 'email' in bad_fields, (
        'Убедитесь, что возвращаются ошибки валидации'
    )


@pytest.mark.django_db
def test_mixed_import(admin_api_client, mixed_excel_file):
    Worker = apps.get_model('core', 'Worker')
    url = reverse('api:workers-import-excel')
    response = admin_api_client.post(
        url, {'file': mixed_excel_file}, format='multipart'
    )
    assert Worker.objects.count() == 1, (
        'Убедитесь, что валидные записи добавляются'
    )
    assert response.status_code == status.HTTP_201_CREATED, (
        'Убедитесь, что если была добавлена хотя бы одна запись, '
        'возвращается ответ 201'
    )
    assert response.json()['Ошибок валидации'] == 1, (
        'Убедитесь, что возвращается верное количество записей '
        'с проблемами валидации'
    )
