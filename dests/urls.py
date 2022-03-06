from django.urls import path, include
from .views import ListDest, DetailDest, CreateDest, DeleteDest, UpdateDest

urlpatterns = [
    path('list', ListDest.as_view()),
    path('detail/<int:pk>', DetailDest.as_view()),
    path('create', CreateDest.as_view()),
    path('delete/<int:pk>', DeleteDest.as_view()),
    path('update/<int:pk>', UpdateDest.as_view()),
]