from django.urls import path
from .views import ListSource, DetailSource

urlpatterns = [
    path('', ListSource.as_view()),
    path('<int:pk>/', DetailSource.as_view()),
]