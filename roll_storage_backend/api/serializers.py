from rest_framework import serializers

from storage.models import Coil


class CoilSerializer(serializers.ModelSerializer):
    """Сериализатор модели рулона."""

    class Meta:
        """Настройки сериализатора модели рулона."""
        model = Coil
        fields = (
            'id',
            'length',
            'weight',
            'add_date',
            'deletion_date',
        )
        read_only_fields = ('add_date', 'deletion_date', )
