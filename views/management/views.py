from views.application.models import Cidade
from .models import Campanha, Onibus, Rota, Passageiro, Administrador
from .forms import CampanhaForm, OnibusForm, RotaForm

from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView
from django.views.generic.edit import CreateView, BaseUpdateView
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib import messages

from django.contrib.auth import get_user_model

User = get_user_model()

# Dashboard
class MainPageView(LoginRequiredMixin, TemplateView):
    """
    View para a página principal do dashboard, acessível apenas por usuários logados.
    Exibe informações sobre os três ônibus mais recentes, campanhas de administração e campanhas de passageiros,
    com base nos dados do usuário logado.
    """
    template_name = "dashboard/dashboard.html"
    login_url = 'v1/auth/login/'

    def get_context_data(self, **kwargs):
        """
        Adiciona os dados ao contexto da view antes de renderizar o template. 
        Esses dados incluem os ônibus mais recentes e as campanhas do administrador e do passageiro, 
        relacionadas ao usuário logado.
        """
        context = super().get_context_data(**kwargs)
        context['onibus'] = Onibus.objects.all().order_by('-ultima_manutencao')[:3]
        context['campanha_adm'] = Campanha.objects.filter(administrador__id_usuario=self.request.user).order_by('-data_criacao')[:3]
        context['campanha_psg'] = Campanha.objects.filter(passageiro__id_usuario=self.request.user).order_by('-data_criacao')[:3]
        return context
    
    def get(self, request, *args, **kwargs):
        """
        Sobrescreve o método GET para renderizar a página principal com o contexto.
        """
        context = self.get_context_data(**kwargs)

        return render(request, self.template_name, context)

# Campanha
class ListarCampanhasView(LoginRequiredMixin, ListView):
    """
    View para listar as campanhas associadas ao usuário logado. 
    O usuário pode visualizar campanhas de sua administração e também campanhas nas quais é passageiro.
    """
    template_name = 'campanha/listar/listarCampanha.html'
    model = Campanha
    
    def get_context_data(self, **kwargs):
        """
        Adiciona os dados ao contexto da view antes de renderizar o template. 
        O contexto inclui campanhas administradas pelo usuário e campanhas nas quais o usuário é passageiro.
        """
        context = super().get_context_data(**kwargs)
        context['campanha_adm'] = Campanha.objects.filter(administrador__id_usuario=self.request.user)
        context['campanha_passageiro'] = Campanha.objects.filter(passageiro__id_usuario=self.request.user)
        return context
    
class AdicionarCampanhaView(LoginRequiredMixin, CreateView):
    """
    View para criar uma nova campanha. Somente usuários autenticados podem acessar esta view.
    Após a criação da campanha, o usuário é atribuído como administrador da campanha automaticamente.
    """
    template_name = 'campanha/adicionar/adicionarCampanha.html'
    model = Campanha
    form_class = CampanhaForm
    success_url = reverse_lazy('listarCampanha')

    def form_valid(self, form):
        """
        Sobrescreve o método form_valid para salvar a campanha e associar o usuário logado 
        como administrador da campanha.
        """
        self.object = form.save(commit=False)

        self.object.criado_por = self.request.user
        self.object.save() 

        Administrador.objects.create(id_usuario=self.request.user, id_campanha=self.object, role='ADM')

        return redirect(self.success_url)

class ExcluirCampanhaView(LoginRequiredMixin, DeleteView):
    """
    View para excluir uma campanha. Somente usuários autenticados podem acessar esta view.
    Após a exclusão da campanha, o usuário será redirecionado para a página de listagem de campanhas.
    """
    model = Campanha
    template_name = 'campanha/excluir/excluirCampanha.html'
    success_url = reverse_lazy('listarCampanha')

class EditarCampanhaView(LoginRequiredMixin, UpdateView):
    """
    View para editar uma campanha existente. Somente usuários autenticados podem acessar esta view.
    Após a edição bem-sucedida da campanha, o usuário será redirecionado para a página de listagem de campanhas.
    """
    model = Campanha
    form_class = CampanhaForm
    template_name = 'campanha/editar/editarCampanha.html'
    success_url = reverse_lazy('listarCampanha')

# Onibus
class ListarOnibusView(LoginRequiredMixin, ListView):
    """
    View para listar os ônibus disponíveis. Somente usuários autenticados podem acessar esta view.
    A lista de ônibus será renderizada no template 'listarOnibus.html'.
    """
    template_name = 'onibus/listar/listarOnibus.html'
    model = Onibus
    
class AdicionarOnibusView(LoginRequiredMixin, CreateView):
    """
    View para adicionar um novo ônibus. Somente usuários autenticados podem acessar esta view.
    Após a criação do ônibus, o usuário será redirecionado para a página de listagem de ônibus.
    """
    template_name = 'onibus/adicionar/adicionarOnibus.html'
    model = Onibus
    form_class = OnibusForm
    success_url = reverse_lazy('listarOnibus')

    def form_valid(self, form):
        """
        Sobrescreve o método form_valid para salvar o ônibus com o usuário logado 
        como criador, antes de redirecionar.
        """
        self.object = form.save(commit=False)
        self.object.criado_por = self.request.user
        print(self.request.user)
        print(self.object.criado_por)
        self.object.save()
        return redirect(self.success_url)

    def form_invalid(self, form):
        """
        Sobrescreve o método form_invalid para renderizar novamente o formulário
        caso haja erro de validação.
        """
        return self.render_to_response(self.get_context_data(form=form))

class EditarOnibusView(LoginRequiredMixin, UpdateView):
    """
    View para editar as informações de um ônibus existente. Somente usuários autenticados podem acessar esta view.
    Após a edição bem-sucedida do ônibus, o usuário será redirecionado para a página de listagem de ônibus.
    """
    model = Onibus
    form_class = OnibusForm
    template_name = 'onibus/editar/editarOnibus.html'

    def get_success_url(self):
        """
        Retorna a URL para onde o usuário será redirecionado após a edição bem-sucedida do ônibus.
        Nesse caso, a página de listagem de ônibus.
        """
        return reverse_lazy('listarOnibus') 

    def get_object(self):
        """
        Sobrescreve o método get_object para recuperar o ônibus a ser editado,
        com base no 'pk' (primary key) fornecido na URL.
        """
        return get_object_or_404(Onibus, pk=self.kwargs['pk'])
    
    def form_valid(self, form):
        """
        Sobrescreve o método form_valid para aplicar lógica adicional antes de salvar as alterações.
        Se o campo 'ultima_manutencao' não for preenchido no formulário, o valor anterior será mantido.
        """
        onibus_form = form.save(commit=False)
        onibus = self.get_object()

        if onibus_form.ultima_manutencao is None:
            onibus_form.ultima_manutencao = onibus.ultima_manutencao
        # print(onibus_form.ultima_manutencao)

        onibus_form.save()
        return super().form_valid(form)
    
class ExcluirOnibusView(LoginRequiredMixin, DeleteView):
    """
    View para excluir um ônibus existente. Somente usuários autenticados podem acessar esta view.
    Após a exclusão bem-sucedida do ônibus, o usuário será redirecionado para a página de listagem de ônibus.
    """
    model = Onibus
    template_name = 'onibus/excluir/excluirOnibus.html'

    def get_success_url(self):
        """
        Retorna a URL para onde o usuário será redirecionado após a exclusão bem-sucedida do ônibus.
        Nesse caso, a página de listagem de ônibus.
        """
        return reverse_lazy('listarOnibus') 

    def get_object(self):
        """
        Sobrescreve o método get_object para recuperar o ônibus a ser excluído,
        com base no 'pk' (primary key) fornecido na URL.
        Se o objeto não for encontrado, lança uma exceção Http404.
        """
        return get_object_or_404(Onibus, pk=self.kwargs['pk'])
    
# Rotas
class ListarRotasView(LoginRequiredMixin, ListView):
    """
    View para listar as rotas associadas a uma campanha específica. Somente usuários autenticados podem acessar esta view.
    A lista de rotas será filtrada com base no ID da campanha fornecido na URL.
    """
    template_name = 'rota/listar/listarRota.html'
    model = Rota

    def get_queryset(self):
        """
        Sobrescreve o método get_queryset para retornar as rotas associadas à campanha especificada na URL.
        Filtra as rotas com base no ID da campanha.
        """
        campanha_id = self.kwargs['campanha_id']
        return Rota.objects.filter(id_campanha=campanha_id) 
    
    def get_context_data(self, **kwargs):
        """
        Sobrescreve o método get_context_data para adicionar dados adicionais ao contexto, como a campanha e o administrador.
        """
        contexto = super().get_context_data(**kwargs)
        campanha_id = self.kwargs['campanha_id']
        contexto['campanha'] = get_object_or_404(Campanha, id=campanha_id)
        contexto['administrador'] = Administrador.objects.filter(id_campanha=campanha_id)
        return contexto
    
class AdicionarRotaView(LoginRequiredMixin, CreateView):
    """
    View para adicionar uma nova rota a uma campanha específica. Somente usuários autenticados podem acessar esta view.
    Após a criação bem-sucedida da rota, o usuário será redirecionado para a página de listagem de rotas da campanha.
    """
    template_name = 'rota/adicionar/adicionarRota.html'
    model = Rota
    form_class = RotaForm

    def get_context_data(self, **kwargs):
        """
        Sobrescreve o método get_context_data para adicionar o contexto da campanha à página de criação da rota.
        A campanha é identificada pelo ID da campanha passado na URL.
        """
        contexto = super().get_context_data(**kwargs)
        contexto['campanha'] = get_object_or_404(Campanha, id=self.kwargs['campanha_id'])
        return contexto

    def get_success_url(self):
        """
        Retorna a URL para onde o usuário será redirecionado após a criação bem-sucedida da rota.
        Neste caso, é a página de listagem de rotas para a campanha específica.
        """
        return reverse_lazy('listarRotas', kwargs={'campanha_id': self.kwargs['campanha_id']})

    def form_valid(self, form):
        """
        Sobrescreve o método form_valid para realizar validações personalizadas antes de salvar a rota.
        Verifica se as cidades de início e fim foram fornecidas e se elas existem no banco de dados.
        """
        cidade_comeco_id = self.request.POST.get('id_rota_comeco')
        cidade_final_id = self.request.POST.get('id_rota_final')

        if not cidade_comeco_id or not cidade_final_id:
            messages.error(self.request, "Cidades não fornecidas")
            return self.form_invalid(form)

        try:
            cidade_comeco = Cidade.objects.get(id=cidade_comeco_id)
            cidade_final = Cidade.objects.get(id=cidade_final_id)
        except Cidade.DoesNotExist:
            messages.error(self.request, "Uma ou ambas as cidades não existem")
            return self.form_invalid(form)

        form.instance.id_rota_comeco = cidade_comeco
        form.instance.id_rota_final = cidade_final

        campanha_atual = get_object_or_404(Campanha, id=self.kwargs['campanha_id'])
        form.instance.id_campanha = campanha_atual

        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        """
        Sobrescreve o método post para manipular as cidades antes da validação do formulário.
        Se as cidades não forem válidas, o formulário será invalidado e a mensagem de erro será exibida.
        """
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)

        messages.error(request, f'{form.errors}')
        return self.form_invalid(form)
    
class EditarRotaView(UpdateView):
    """
    View para editar uma rota associada a uma campanha específica. Somente usuários autenticados podem acessar esta view.
    Após a edição bem-sucedida da rota, o usuário será redirecionado para a página de listagem de rotas da campanha.
    """
    template_name = 'rota/editar/editarRota.html'    
    model = Rota
    form_class = RotaForm

    def get_context_data(self, **kwargs):
        """
        Sobrescreve o método get_context_data para adicionar o contexto da campanha à página de edição da rota.
        A campanha é identificada pelo ID da campanha passado na URL.
        """
        contexto = super().get_context_data(**kwargs)
        contexto['campanha'] = get_object_or_404(Campanha, id=self.kwargs['campanha_id'])
        return contexto

    def get_success_url(self):
        """
        Retorna a URL para onde o usuário será redirecionado após a edição bem-sucedida da rota.
        Neste caso, é a página de listagem de rotas para a campanha específica.
        """
        return reverse_lazy('listarRotas', kwargs={'campanha_id': self.kwargs['campanha_id']})
    
class ExcluirRotaView(LoginRequiredMixin, DeleteView):
    """
    View para excluir uma rota associada a uma campanha específica. Somente usuários autenticados podem acessar esta view.
    Após a exclusão bem-sucedida da rota, o usuário será redirecionado para a página de listagem de rotas da campanha.
    """
    model = Rota
    template_name = 'rota/excluir/excluirRota.html'
    
    def get_success_url(self):
        """
        Retorna a URL para onde o usuário será redirecionado após a exclusão bem-sucedida da rota.
        Neste caso, é a página de listagem de rotas para a campanha específica.
        """
        return reverse_lazy('listarRotas', kwargs={'campanha_id': self.kwargs['campanha_id']})

# Equipe
class ListarEquipeView(LoginRequiredMixin, ListView):
    """
    View para listar a equipe de uma campanha específica. Somente usuários autenticados podem acessar esta view.
    A equipe inclui administradores e passageiros associados à campanha especificada pelo ID.
    """
    template_name = 'equipe/listar/listarEquipe.html'
    model = User

    def get_context_data(self, **kwargs):
        """
        Sobrescreve o método get_context_data para adicionar a campanha e os membros da equipe (administradores e passageiros) ao contexto.
        A campanha é identificada pelo ID passado na URL.
        """
        context = super().get_context_data(**kwargs)
        campanha_id = self.kwargs['campanha_id']

        campanha = get_object_or_404(Campanha, id=campanha_id)
        context['campanha'] = campanha

        context['administradores'] = Administrador.objects.filter(id_campanha=campanha)
        context['passageiros'] = Passageiro.objects.filter(id_campanha=campanha)
        return context

class AdicionarEquipeView(LoginRequiredMixin, CreateView):
    """
    View para adicionar um novo membro à equipe de uma campanha. O membro pode ser um motorista (administrador) ou um passageiro.
    Somente usuários autenticados podem acessar essa view.
    """
    template_name = 'equipe/adicionar/adicionarEquipe.html'
    
    def get_success_url(self):
        """
        Retorna a URL de sucesso após a adição do membro à equipe. O redirecionamento é feito para a listagem da equipe da campanha.
        """
        return reverse_lazy('listarEquipe', kwargs={'campanha_id': self.kwargs['campanha_id']})
    
    def get(self, request, campanha_id):
        """
        Sobrescreve o método GET para carregar o template de adicionar equipe, passando a campanha associada.
        """
        campanha = get_object_or_404(Campanha, id=campanha_id)
        return render(request, self.template_name, {'campanha': campanha})

    def post(self, request, campanha_id):
        """
        Sobrescreve o método POST para processar a adição de um novo membro à equipe. 
        O membro pode ser um motorista ou um passageiro.
        """
        campanha = get_object_or_404(Campanha, id=campanha_id)
        user_id = request.POST.get('user_id')
        is_motorista = request.POST.get('is_motorista')
        role = request.POST.get('role') if is_motorista else None
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            # Mensagem de erro caso o usuário não seja encontrado
            messages.error(request, "Usuário não encontrado.")
            return redirect('adicionarEquipe', campanha_id=campanha_id)
        
        if is_motorista:
            # Se for motorista, cria o Administrador com o papel adequado
            if role:
                administrado = Administrador(id_usuario=user, id_campanha=campanha, role=role)
                administrado.save()
                messages.success(request, f"Motorista {user.first_name} adicionado com sucesso.")
            else:
                messages.error(request, "Função não selecionada para o motorista.")
        else:
            # Se for passageiro
            passageiro = Passageiro(id_usuario=user, id_campanha=campanha)
            passageiro.save()
            messages.success(request, f"Passageiro {user.first_name} adicionado com sucesso.")

        return redirect('listarEquipe', campanha_id=campanha_id)

## SubEquipe / Remover Usuario da Equipe    
class RemoverAdministradorView(LoginRequiredMixin, DeleteView):
    """
    View para remover um administrador da equipe de uma campanha. Somente usuários autenticados podem acessar esta view.
    O administrador será removido da campanha especificada e o sistema redireciona para a listagem da equipe.
    """
    template_name = 'equipe/remover/administrador/removerEquipe.html'
    model = Administrador
    success_url = reverse_lazy('listarEquipe')

    def get_context_data(self, **kwargs):
        """
        Sobrescreve o método get_context_data para incluir o contexto adicional:
        - Detalhes da campanha da qual o administrador será removido.
        - O administrador a ser removido.
        """
        context = super().get_context_data(**kwargs)
        
        campanha_id = self.kwargs.get('campanha_id')
        context['campanha'] = get_object_or_404(Campanha, id=campanha_id)
        context['administrador'] = get_object_or_404(Administrador, pk=self.kwargs['pk'])
        return context
    
    def get_success_url(self):
        """
        Sobrescreve o método get_success_url para redirecionar para a listagem de equipe após a remoção do administrador.
        """
        return reverse_lazy('listarEquipe', kwargs={'campanha_id': self.kwargs['campanha_id']})
    
class RemoverPassageiroView(LoginRequiredMixin, DeleteView):
    """
    View para remover um passageiro da equipe de uma campanha. Somente usuários autenticados podem acessar esta view.
    O passageiro será removido da campanha especificada e o sistema redireciona para a listagem da equipe.
    """
    template_name = 'equipe/remover/passageiro/removerEquipe.html'
    model = Passageiro
    success_url = reverse_lazy('listarEquipe')

    def get_context_data(self, **kwargs):
        """
        Sobrescreve o método get_context_data para incluir o contexto adicional:
        - Detalhes da campanha da qual o passageiro será removido.
        - O passageiro a ser removido.
        """
        context = super().get_context_data(**kwargs)
        
        campanha_id = self.kwargs.get('campanha_id')
        context['campanha'] = get_object_or_404(Campanha, id=campanha_id)
        context['passageiro'] = get_object_or_404(Passageiro, pk=self.kwargs['pk'])
        return context
    
    def get_success_url(self):
        """
        Sobrescreve o método get_success_url para redirecionar para a listagem de equipe após a remoção do passageiro.
        """
        return reverse_lazy('listarEquipe', kwargs={'campanha_id': self.kwargs['campanha_id']})
    