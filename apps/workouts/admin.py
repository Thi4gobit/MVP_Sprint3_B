from django.contrib import admin 
from .models import Workout


class WorkoutAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'date', 'city', 'state', 'kilometers', 
        'duration', 'frequency', 'kcal', 'speed'
    )
    search_fields = ['date']
    list_filter = ['state']


admin.site.register(Workout, WorkoutAdmin)