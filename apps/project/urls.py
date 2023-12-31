from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('forms', create_vaga, name="form"),
    path('<int:vaga_id>/view-vaga', view_vaga, name="view_vaga"),
    path('<int:vaga_id>/change-vaga', change_vaga, name="change_vaga"),
    path('search', search, name="search"),
    path('<int:vaga_id>/delete-vaga', delete_job, name="delete_vaga"),
    path('dashboard', minhas_vagas, name="minhas_vagas"),
    path('inscrever/<int:vaga_id>', inscrever_aluno, name="inscrever_aluno"),
    path('retirar/<int:vaga_id>', desinscrever_aluno, name='retirar_inscricao'),
    path('vagas-inciacao-cietifica', projeto_tecnologico,
         name='projeto_tecnologico'),
    path('vagas-pesquisa', projeto_cientifico, name='projeto_cientifico'),
    path('vagas-extensao', projeto_extencao, name='projeto_extencao'),
    path('vagas-estagio', estagio, name="vagas_estagio"),
    path('vagas-desenvolvimento', projeto_desenvolvimento,
         name="projeto_desenvolvimento"),
    path('filter-area/<str:area>', filter_area,
         name="filter_area"),
    # path('new-card', new_cards, name="new-cards")
]
