from .views import RegisterView, UserLoginView, ProfileView, AddressEditionView, AddressRemoveView, AddressAddView, ListProfileView, RemoveProfileView, ChangePasswordProfileView
from controller import settings

# Bibliotecas
from django.contrib.auth.views import LogoutView
from django.urls import path

# from core.views import signup, login_auth

urlpatterns = [
    # Acessar Usuário
    path("register/", RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
] + [
    # Edit User Endereco
    path('edit/editProfile/<str:id>/AddEndereco/', AddressAddView.as_view(), name='addAdress'),
    path('edit/editProfile/<str:id>/EditEndereco/<int:endereco_id>', AddressEditionView.as_view(), name='editAdress'),
    path('edit/editProfile/<str:id>/RemoveEndereco/<int:endereco_id>', AddressRemoveView.as_view(), name='removeAddress')
] + [
    # Edit Profile
    path('edit/editProfile/<str:id>', ProfileView.as_view(), name='editProfile'),
    path('list/listProfile/<str:id>/<str:usuario>', ListProfileView.as_view(), name='listProfile'),
    path('remove/removeProfile/<str:id>/', RemoveProfileView.as_view(), name='removeProfile'),
    path('changepassword/passwordProfile/<str:id>', ChangePasswordProfileView.as_view(), name='passwordProfile')
]