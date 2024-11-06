from django.urls import path
from . import views

urlpatterns = [
    # rotas abertas
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('tipos/', views.list_tipos, name='list_tipos'),

# rotas fechadas

    ## Rota de imóveis
    path('tipos/adicionar/', views.adicionar_tipo, name='adicionar_tipo'),
    path('tipos/editar/<int:tipo_id>', views.editar_tipo, name='editar_tipo'),
    path('tipos/excluir/<int:tipo_id>', views.excluir_tipo, name='excluir_tipo'),
    path('tipos/detalhar_tipo/<int:tipo_id>', views.detalhar_tipo, name='detalhar_tipo'),
]