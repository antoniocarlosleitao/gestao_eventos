from django.urls import path
from . import views

urlpatterns = [
    # rotas abertas
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('eventos/', views.listar_eventos, name='listar_eventos'),

# rotas fechadas
    path('conferencias/',views.ListConferenciaView.as_view(), name='list_conferencia'),
    path('palestras/', views.ListPalestraView.as_view(), name='list_palestra'),
    path('workshops/', views.ListWorkshopView.as_view(), name='list_workshop'),

    ## Rota de eventos
    path('eventos/adicionar/', views.adicionar_evento, name='adicionar_evento'),
    path('eventos/editar/<int:evento_id>', views.editar_evento, name='editar_evento'),
    path('eventos/excluir/<int:evento_id>', views.excluir_evento, name='excluir_evento'),
    path('eventos/detalhar_evento/<int:evento_id>', views.detalhar_evento, name='detalhar_evento'),

# Rota de consulta de CEP
    path('buscar-endereco/', views.buscar_endereco, name='buscar_endereco'),
]

