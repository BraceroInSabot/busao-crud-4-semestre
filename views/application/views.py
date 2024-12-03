# Bibliotecas
from django.shortcuts import render
from django.views import View
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from .models import Cidade

User = get_user_model()

class HomePage(View):
    """
    View para exibir a página inicial do site. Renderiza o template 'homepage/index.html'.
    A view passa um contexto com todos os usuários (User) registrados no sistema.
    """
    template_name = 'homepage/index.html'

    def get(self, request, *args, **kwargs):
        """
        Renderiza o template com o contexto fornecido, que inclui a lista de usuários.
        """
        return render(request, self.template_name, {'log_user': User})
    

class CityAutocompleteView(View):
    """
    View para implementar a funcionalidade de autocompletar na busca por cidades.
    Recebe o termo digitado pelo usuário e retorna até 10 sugestões de cidades que
    correspondem ao que foi digitado.
    """
    
    def get(self, request, *args, **kwargs):
        query = request.GET.get('term', '')  # Captura o termo digitado
        if query:
            cidades = Cidade.objects.filter(nome__icontains=query).values_list('nome', flat=True)[:10]
            # print(cidades)
            return JsonResponse(list(cidades), safe=False)
        return JsonResponse([], safe=False)
        