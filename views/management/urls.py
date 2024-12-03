from .views import (MainPageView, ListarCampanhasView, AdicionarCampanhaView, 
                    AdicionarOnibusView, ListarOnibusView, EditarOnibusView, 
                    ExcluirOnibusView, ListarRotasView, AdicionarRotaView,
                    EditarRotaView, ExcluirRotaView, ListarEquipeView,
                    AdicionarEquipeView, ExcluirCampanhaView, EditarCampanhaView, 
                    RemoverAdministradorView, RemoverPassageiroView)

# Bibliotecas
from django.urls import path

# from core.views import signup, login_auth

urlpatterns = [
    # Classes / POO
    path("", MainPageView.as_view(), name="dashboard"),
] + [
    # Campanhas
    path('listarCampanhas/', ListarCampanhasView.as_view(), name='listarCampanha'),
    path('adicionarCampanha/', AdicionarCampanhaView.as_view(), name='adicionarCampanha'),
    path('excluirCampanha/<slug:pk>', ExcluirCampanhaView.as_view(), name='excluirCampanha'),
    path('editarCampanha/<slug:pk>', EditarCampanhaView.as_view(), name='editarCampanha'),
] + [
    # Onibus
    path('listarOnibus/', ListarOnibusView.as_view(), name='listarOnibus'),
    path('adicionarOnibus/', AdicionarOnibusView.as_view(), name='adicionarOnibus'),
    path('editarOnibus/<slug:pk>', EditarOnibusView.as_view(), name='editarOnibus'),
    path('excluirOnibus/<slug:pk>', ExcluirOnibusView.as_view(), name='excluirOnibus')
] + [
    # Rotas
    path('listarRotas/Campanha-<int:campanha_id>', ListarRotasView.as_view(), name='listarRotas'),
    path('adicionarRota/Campanha-<int:campanha_id>', AdicionarRotaView.as_view(), name='adicionarRota'),
    path('editarRota/Campanha-<int:campanha_id>/Rota-<int:pk>', EditarRotaView.as_view(), name='editarRota'),
    path('excluirRota/Campanha-<int:campanha_id>/Rota-<int:pk>', ExcluirRotaView.as_view(), name='excluirRota'),
] + [
    # Equipe
    path('listarEquipe/Campanha-<int:campanha_id>', ListarEquipeView.as_view(), name='listarEquipe'),
    path('adicionarEquipe/Campanha-<int:campanha_id>', AdicionarEquipeView.as_view(), name='adicionarEquipe'),
    path('removerEquipe/Campanha-<int:campanha_id>/Administrador-<slug:pk>', RemoverAdministradorView.as_view(), name='removerAdministrador'),
    path('removerEquipe/Campanha-<int:campanha_id>/Passageiro-<slug:pk>', RemoverPassageiroView.as_view(), name='removerPassageiro'),
]