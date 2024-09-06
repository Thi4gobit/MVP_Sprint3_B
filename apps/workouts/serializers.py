from rest_framework import serializers
from .models import Workout
from datetime import timedelta
from datetime import date

class WorkoutSerializer(serializers.ModelSerializer):

    duration = serializers.SerializerMethodField()

    class Meta:
        model = Workout
        fields = '__all__'

    def get_duration(self, obj):
        total_seconds = obj.duration.total_seconds()
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f'{int(hours)}:{int(minutes)}:{int(seconds)}'
    
    def validate_duration(self, value):
        if value < timedelta(seconds=0):
            raise serializers.ValidationError("A duração não pode ser negativa.")
        return value
    
    def validate_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("A data não pode ser no futuro.")
        return value
