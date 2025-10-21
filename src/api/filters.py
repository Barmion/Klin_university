import django_filters

from core.models import Worker


class WorkerFilter(django_filters.FilterSet):
    position = django_filters.CharFilter(
        field_name='position__name',
        lookup_expr='icontains',
        label='Название должности',

    )

    class Meta:
        model = Worker
        fields = ['is_active', 'position',]
