from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api.filters import WorkerFilter
from api.permissions import AdminOrReadOnly
from api.schemas import IMPORT_EXCEL_SCHEMA
from api.serializers import WorkerListSerializer, WorkerSerializer
from core.models import Worker
from core.services import parse_excel, validate_uploaded_file


class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.select_related('position',)
    permission_classes = [AdminOrReadOnly,]
    filter_backends = [DjangoFilterBackend]
    filterset_class = WorkerFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return WorkerListSerializer
        return WorkerSerializer

    @extend_schema(**IMPORT_EXCEL_SCHEMA)
    @action(['post'], detail=False, url_path='import')
    def import_excel(self, request, *args, **kwargs):
        try:
            file = validate_uploaded_file(request)
            records = parse_excel(file)
            results = {
                'Записей добавлено': 0,
                'Добавленые записи': [],
                'Ошибок валидации': 0,
                'Записи с ошибками': [],
            }

            for record in records:
                serializer = self.get_serializer(data=record)
                if serializer.is_valid():
                    serializer.save()
                    results['Записей добавлено'] += 1
                    results['Добавленые записи'].append(serializer.data)
                else:
                    results['Ошибок валидации'] += 1
                    results['Записи с ошибками'].append(
                        (serializer.data, serializer.errors)
                    )

            return Response(
                results,
                status=(
                    status.HTTP_201_CREATED
                    if results['Записей добавлено']
                    else status.HTTP_400_BAD_REQUEST
                )
            )
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
