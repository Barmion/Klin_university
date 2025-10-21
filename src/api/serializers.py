from rest_framework import serializers

from core.models import Worker, Position


class WorkerSerializer(serializers.ModelSerializer):
    position = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Position.objects.all(),
    )
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Worker
        fields = (
            'id',
            'last_name',
            'first_name',
            'middle_name',
            'email',
            'position',
            'is_active',
            'created_by',
            'hired_date',
        )
        read_only_fields = (
            'hired_date',
        )

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class WorkerListSerializer(serializers.ModelSerializer):
    position = serializers.StringRelatedField()

    class Meta:
        model = Worker
        fields = (
            'id',
            'last_name',
            'first_name',
            'middle_name',
            'position',
            'is_active',
        )
