from django.urls import path, include
from .views import ListSource, DetailSource, CreateSource, DeleteSource, UpdateSource

urlpatterns = [
    path('list', ListSource.as_view()),
    path('<int:pk>', DetailSource.as_view()),
    path('create', CreateSource.as_view()),
    path('delete/<int:pk>', DeleteSource.as_view()),
    path('update/<int:pk>', UpdateSource.as_view()),
]