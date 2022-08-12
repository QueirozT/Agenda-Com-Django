from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),  # Chamando a view index do contatos
]