from django.urls import path
from .views import *


urlpatterns = [
    path('get', get, name='workout_get'),
    path('post', post, name='workout_post'),
    path('update/<int:pk>', update, name='workout_update'),
    path('delete/<int:pk>', delete, name='workout_delete'),
]