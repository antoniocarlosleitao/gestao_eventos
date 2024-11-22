from django.urls import path
from . import views

urlpatterns = [
    # rotas abertas
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('eventos/', views.listar_eventos, name='list_tipos'),

# rotas fechadas

    ## Rota de eventos
    path('eventos/adicionar/', views.adicionar_evento, name='adicionar_evento'),
    path('eventos/editar/<int:evento_id>', views.editar_evento, name='editar_evento'),
    path('eventos/excluir/<int:evento_id>', views.excluir_evento, name='excluir_evento'),
    path('eventos/detalhar_evento/<int:evento_id>', views.detalhar_evento, name='detalhar_evento'),
]