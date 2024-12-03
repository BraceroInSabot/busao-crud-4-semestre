from django.urls import path
from .views import HomePage, CityAutocompleteView

# from core.views import signup, login_auth

urlpatterns = [
    # Classes / POO
    path("", HomePage.as_view(), name="home"),
    path('autocomplete/cidades/', CityAutocompleteView.as_view(), name='autocomplete-cidades'),
    # path("/OnibusListagem", PageView.as_view(template_name="page.html"), name="page")

    # # Functions
    # path("signup/", signup, name="signup"),
    # path("login/", login_auth, name="login"),
]