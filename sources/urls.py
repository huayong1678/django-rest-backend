from django.urls import path, include
from .views import ListSource, DetailSource, CreateSource, DeleteSource

urlpatterns = [
    path('list', ListSource.as_view()),
    path('detail/<int:pk>', DetailSource.as_view()),
    path('create', CreateSource.as_view()),
    path('delete/<int:pk>', DeleteSource.as_view()),
]