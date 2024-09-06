from django.contrib import admin 
from .models import Workout, State


class StateAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'code')


class WorkoutAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'date', 'state', 'kilometers', 'duration', 'bpm', 'kcal'
    )
    search_fields = ['date']
    list_filter = ['state']


admin.site.register(State, StateAdmin)
admin.site.register(Workout, WorkoutAdmin)