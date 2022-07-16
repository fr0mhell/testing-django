from django.urls import path

from . import views

app_name = 'trainings'

urlpatterns = [
    path('', views.index, name='index'),
    path('my-trainings/', views.my_trainings, name='my-trainings'),
    path('create-profile/', views.create_profile, name='create-profile')
]