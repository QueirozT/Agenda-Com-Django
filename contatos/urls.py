from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Chamando a view index do contatos
    path('busca/', views.busca, name='busca'),
    path('<int:contato_id>', views.detalhes, name='detalhes'),
]
