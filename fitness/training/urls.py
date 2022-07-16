from django.urls import path

from . import views

app_name = 'trainings'

urlpatterns = [
    path('', views.index, name='index'),
    path('my-trainings/', views.my_trainings, name='my-trainings'),

    path('profile/', views.create_profile, name='create-profile'),
    path('profile/<int:profile_id>/', views.edit_profile, name='edit-profile'),

    path('training/', views.add_training, name='create-training'),
    path('training/<int:training_id>/', views.edit_training, name='edit-training'),
]