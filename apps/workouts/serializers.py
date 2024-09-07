from rest_framework import serializers
from .models import Workout
from datetime import timedelta, date


class WorkoutSerializer(serializers.ModelSerializer):

    duration = serializers.CharField()

    class Meta:
        model = Workout
        fields = '__all__'

    def to_representation(self, instance):
        """Converte o objeto do modelo para um formato serializado"""
        representation = super().to_representation(instance)
        total_seconds = instance.duration.total_seconds()
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        representation['duration'] = \
            f'{int(hours):02}:{int(minutes):02}:{int(seconds):02}'
        return representation

    def to_internal_value(self, data):
        """Converte (string HH:MM:SS) para o formato timedelta"""
        internal_value = super().to_internal_value(data)
        duration_str = data.get('duration')
        try:
            hours, minutes, seconds = map(int, duration_str.split(':'))
            duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
            if duration < timedelta(seconds=0):
                raise serializers.ValidationError(
                    {"error": "A duração não pode ser negativa."}
                )
            internal_value['duration'] = duration
        except ValueError:
            raise serializers.ValidationError(
                {"error": "Formato inválido. Use HH:MM:SS."}
            )
        return internal_value

    def validate_date(self, value):
        """Valida se a data não está no futuro"""
        if value > date.today():
            raise serializers.ValidationError(
                {"error": "A data não pode ser no futuro."}
            )
        return value
