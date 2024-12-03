# Projeto
from .forms import UsuarioForm, AddressForm, EditUsuarioForm, RemoveUsuarioReasonForm
from views.application.models import Cidade, Endereco
from views.userAuth.models import DeactivateReason, Usuario_Desativacao

# Bibliotecas
import traceback
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, CreateView, UpdateView, BaseUpdateView, DeleteView
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import Http404
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth.forms import PasswordChangeForm


User = get_user_model()

def save(self, commit=True) -> object:
    """Sobrescreve o método save() para o tratamento de imagem quando for editar o perfil.

    Args:
        commit (bool, optional): Permite não adicionar quando chamado o método. Verdadeiro por padrão.

    Returns:
        user: Modelo Usuário padrão do sistema com imagem informada.
    """
    user = super().save(commit=False)
    
    if self.cleaned_data.get('imagem'):
        user.imagem = self.cleaned_data['imagem']
    
    if commit:
        user.save()
    return user

# Autenticação
class RegisterView(CreateView):
    """
    View para registro de um novo usuário. Esta view exibe um formulário de registro,
    cria o usuário, realiza a autenticação e redireciona para a página de sucesso 
    (home).
    """
    template_name = 'register/register.html'
    form_class = UsuarioForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """
        Este método é chamado quando o formulário de registro é válido.
        Ele cria um novo usuário, define a senha de forma segura, autentica 
        o usuário e o faz login automaticamente. Caso a autenticação falhe, 
        uma mensagem de erro será exibida.
        """

        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()

        username = form.cleaned_data['usuario']
        password = form.cleaned_data['password1']
        user_login = authenticate(self.request, username=username, password=password)

        if user_login:
            login(self.request, user_login)
        else:
            messages.error(self.request, "Erro ao autenticar. Por favor, faça login manualmente.")
        
        return redirect(self.success_url)
        
    
    def post(self, request, *args, **kwargs):
        """
        Manipula a requisição POST. Se o formulário for válido, chama o método `form_valid`.
        Caso contrário, chama o método `post` da classe pai para tratar o formulário.
        """
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        return super().post(request, *args, **kwargs)

class UserLoginView(LoginView):
    """
    View personalizada para o login de usuários. Se o usuário já estiver autenticado,
    ele será redirecionado automaticamente para a página de sucesso (dashboard).
    Caso contrário, o formulário de login será exibido.
    """
    
    # Define o template para a página de login.
    template_name = 'login/login.html'
    
    # Define a URL de redirecionamento após o login bem-sucedido.
    success_url = reverse_lazy('dashboard')

    def get(self, request, *args, **kwargs):
        """
        Manipula a requisição GET. Se o usuário já estiver autenticado, ele será
        redirecionado para a URL de sucesso (dashboard). Caso contrário, o formulário
        de login será exibido.
        """
        
        # Verifica se o usuário já está autenticado
        if request.user.is_authenticated:
            # Se o usuário estiver autenticado, redireciona para a página de sucesso
            return redirect(self.success_url)
        
        # Caso contrário, chama o método 'get' da classe pai para exibir o formulário de login
        return super().get(request, *args, **kwargs)

# Usuário
class ProfileView(BaseUpdateView):
    """
    View para edição do perfil do usuário logado. Permite que o usuário altere suas informações 
    pessoais, como nome, email e outros dados. Além disso, associa o usuário a um endereço 
    e permite que ele atualize essas informações também.
    """
    
    template_name = "profile/editar/editProfile.html"
    model = User
    form_class = EditUsuarioForm

    def get_success_url(self):
        """
        Retorna a URL de sucesso após a atualização do perfil. 
        O usuário será redirecionado para a página de visualização do perfil.
        """
        user_id = self.kwargs['id']   
        return reverse_lazy('listProfile', kwargs={'id': user_id, 'usuario': self.request.user.usuario})
    
    def get_object(self, queryset=None):
        """
        Obtém o objeto do usuário logado. Esse método é sobrescrito para garantir que o 
        usuário editando o perfil seja sempre o usuário logado.
        """
        return get_object_or_404(User, id=self.request.user.id)

    def get_context_data(self, **kwargs):
        """
        Adiciona informações adicionais ao contexto, como o endereço do usuário.
        Se o usuário possui um endereço associado, ele é adicionado ao contexto.
        """
        context = super().get_context_data(**kwargs)

        endereco = None
        if hasattr(self.request.user, 'endereco_id') and self.request.user.endereco_id:
            endereco = Endereco.objects.filter(pk=self.request.user.endereco_id).first()
        context['address'] = endereco

        context['object'] = self.object
        return context
    
    def form_valid(self, form):
        """
        Processa o formulário quando ele é validado com sucesso. 
        O endereço do usuário é preservado durante a atualização dos dados.
        """
        logged_user = form.save(commit=False)
        logged_user.endereco = self.request.user.endereco
        logged_user.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        """
        Processa a requisição POST. Quando o formulário é submetido, 
        se for válido, salva as informações e redireciona o usuário.
        Caso contrário, renderiza o template de edição com os erros do formulário.
        """
        self.object = self.get_object()

        form = self.form_class(request.POST, request.FILES, instance=self.object)

        if form.is_valid():
            form.save()
            messages.success(request, "Dados cadastrais atualizados com sucesso!")
            return redirect(self.get_success_url())
        else:
            return render(request, self.template_name, {
                'form': form,
                'address': Endereco.objects.filter(pk=self.request.user.endereco_id).first()
            })

        
    def get(self, request, *args, **kwargs):
        """
        Exibe o formulário de edição do perfil. Retorna o template com o endereço do usuário 
        no contexto, caso haja um registrado.
        """
        return render(request, self.template_name, {'address': Endereco.objects.filter(pk=self.request.user.endereco_id).first()})

class ListProfileView(TemplateView):
    """
    View para exibição das informações do perfil do usuário. Esta view mostra 
    os dados do usuário logado, incluindo o endereço associado, e exibe um template 
    com essas informações.
    """
    template_name = 'profile/listar/listProfile.html'

    def get_success_url(self):
        """
        Retorna a URL de sucesso. Após uma ação bem-sucedida, o usuário será redirecionado 
        para a página de exibição de perfil, utilizando o ID e nome do usuário como parâmetros.
        """
        user_id = self.kwargs['id']  
        user_name = self.kwargs['nome']
        return reverse_lazy('listProfile', kwargs={'id': user_id, 'nome': user_name})
    
    def get_context_data(self, **kwargs):
        """
        Adiciona informações adicionais ao contexto da view. 
        Adiciona o endereço do usuário logado ao contexto, se disponível.
        """
        context = super().get_context_data(**kwargs)

        endereco = None
        if hasattr(self.request.user, 'endereco_id') and self.request.user.endereco_id:
            endereco = Endereco.objects.filter(pk=self.request.user.endereco_id).first()
        context['address'] = endereco
        return context
    
class RemoveProfileView(BaseUpdateView):
    """
    View para desativar o perfil de um usuário. Permite que o usuário forneça um motivo
    para a desativação e processa essa solicitação, desativando a conta do usuário e salvando o motivo
    da desativação no banco de dados.
    """
    template_name = 'profile/excluir/removeProfile.html'
    model = User
    success_url = 'home'
    form_class = RemoveUsuarioReasonForm

    def get_object(self, queryset=None):
        """
        Obtém o objeto do usuário. Este método sobrescrito garante que sempre será obtido
        o usuário para desativação.
        """
        return get_object_or_404(User)
    
    def post(self, request, *args, **kwargs):
        """
        Processa o formulário enviado pelo usuário para desativar a conta. 
        Cria um registro de desativação e marca o usuário como inativo.
        """
        # reason
        print(request.POST)
        print(request.user.is_active)
        form = self.form_class(request.POST)

        if form.is_valid():
            choice_reason = form.cleaned_data.get('choice_reason')
            reason = form.cleaned_data.get('reason') if choice_reason == "OU" else None


            print(form.cleaned_data.get('reason')) 

            deactivate_reason = DeactivateReason.objects.create(
                choice_reason=choice_reason,
                reason=reason
            )
            Usuario_Desativacao.objects.create(
            codigousuario=request.user,
            codigodesativacao=deactivate_reason
        )

            request.user.is_active = False
            request.user.save()
            print('valido')
            return redirect(self.success_url)
        else:
            print('invalido')
            messages.error(request, f'{form.errors}')
            return render(request, self.template_name, {})
        
    def get(self, request, *args, **kwargs):
        """
        Exibe o template de remoção de perfil. 
        Este método é chamado quando o usuário acessa a página para desativar sua conta.
        """
        return render(request, self.template_name)
    
class ChangePasswordProfileView(SuccessMessageMixin, PasswordChangeView):
    """
    View para permitir que o usuário altere sua senha. Esta view exibe um formulário de mudança 
    de senha e, após a alteração bem-sucedida, exibe uma mensagem de sucesso e redireciona o usuário
    para a página de seu perfil.
    """
    template_name = 'profile/passwordChange/passwordProfile.html'
    form_class = PasswordChangeForm
    success_message = "Sua senha foi alterada com sucesso!"
    
    def get_success_url(self):
        """
        Retorna a URL de sucesso após a alteração da senha. O usuário será redirecionado
        para a página de visualização de perfil após a alteração da senha.
        """
        user_id = self.kwargs['id'] 
        return reverse_lazy('listProfile', kwargs={'id': user_id, 'usuario': self.request.user.usuario})

# Endereço (Listagem no perfil do usuário)
class AddressAddView(CreateView):
    """
    View para adicionar um novo endereço ao perfil do usuário. Redireciona para um formulário de 
    criação de endereço e, após a submissão bem-sucedida, salva o endereço associado ao usuário 
    e redireciona para a página do perfil.
    """
    template_name = "address/adicionar/addProfile.html"
    model = Endereco
    form_class = AddressForm

    def get_success_url(self):
        """
        Retorna a URL de sucesso após a adição do endereço. O usuário será redirecionado 
        para a página de exibição do perfil.
        """
        user_id = self.kwargs['id'] 
        return reverse_lazy('listProfile', kwargs={'id': user_id, 'usuario': self.request.user.usuario})
    
    def form_valid(self, form):
        """
        Processa o formulário quando ele é validado com sucesso. 
        Associa o endereço criado ao usuário logado e salva os dados.
        """
        endereco = form.save(commit=False)
        endereco.user = self.request.user 
        endereco.save()
        return super().form_valid(form)
    
    def post(self, request, *args, **kwargs):
        """
        Processa a requisição POST. Se o formulário de endereço for enviado, 
        chama o método `handle_address_form` para processar os dados. Caso contrário, 
        retorna um erro JSON se o formulário não for reconhecido.
        """
        if request.POST:
            print('aaa')
            return self.handle_address_form(request)
        else:
            return JsonResponse({"success": False, "message": "Formulário desconhecido enviado."})
        
    def handle_address_form(self, request):
        """
        Processa o formulário de endereço, associando o endereço criado ao usuário 
        logado e atualizando o perfil do usuário com o ID do novo endereço.
        """
        form = AddressForm(request.POST)
        if form.is_valid():
            endereco = form.save(commit=False)
            endereco.cidade = form.cleaned_data['cidade']
            endereco.save()
            
            # print(endereco.id)
            # Atribui o id do endereco para o perfil do usuário logado
            req_user = User.objects.filter(id=request.user.id).update(endereco_id=endereco.id)
            # print(req_user)

            return self.get(self.get_success_url())
        messages.error(request, f'{form.errors}')
        return render(self.get_success_url)
    
class AddressEditionView(BaseUpdateView):
    """
    View para editar o endereço associado ao perfil do usuário logado. 
    Redireciona para o formulário de Endereço com as informações no campo 
    para editar o objeto e, após a submissão bem-sucedida, 
    salva as alterações e redireciona para a página de edição do perfil.
    """
    template_name = "address/editar/editProfile.html"
    model = Endereco
    form_class = AddressForm
    
    def get_success_url(self):
        """
        Retorna a URL de sucesso após a edição do endereço. 
        O usuário será redirecionado para a página de edição do perfil após salvar o endereço.
        """
        user_id = self.kwargs['id'] 
        return reverse_lazy('editProfile', kwargs={'id': user_id})

    def get_object(self, queryset=None):
        """
        Obtém o objeto do endereço a ser editado. Este método é sobrescrito para garantir 
        que o endereço a ser editado pertence ao usuário logado.
        """
        pk = self.kwargs.get('endereco_id')
        return get_object_or_404(Endereco, pk=pk, user=self.request.user)

    def form_valid(self, form):
        """
        Processa o formulário quando ele é validado com sucesso. 
        Associa o endereço editado ao usuário logado e salva as alterações.
        """
        # Salva as alterações no endereço
        endereco = form.save(commit=False)
        endereco.user = self.request.user  # Garante associação ao usuário logado
        endereco.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Adiciona o objeto de endereço ao contexto da view. 
        Esse objeto é necessário para exibir os dados de endereço nos campos do formulário.
        """
        context = super().get_context_data(**kwargs)
        context['address'] = self.get_object()
        return context
    
    def get(self, request, *args, **kwargs):
        """
        Exibe o formulário de edição do endereço. 
        O endereço a ser editado é passado para o arquivo HTML.
        """
        return render(request, self.template_name, {'address': self.get_object()})

    def post(self, request, *args, **kwargs):
        """
        Processa o formulário enviado para editar o endereço. 
        Se o formulário for válido, as alterações são salvas e o usuário é redirecionado para a página de sucesso.
        Caso contrário, o formulário com erros é renderizado novamente.
        """
        self.object = self.get_object() 

        form = self.form_class(request.POST, instance=self.object)
        
        print(form)
        if form.is_valid():
            # Exclui a imagem antiga se uma nova for enviada

            form.save()  # Salva o formulário
            messages.success(request, "Dados do endereço atualizados com sucesso!")
            return redirect(self.get_success_url())
        else:
            return render(request, self.template_name, {'form': self.get_context_data(form=form), 'address': Endereco.objects.filter(pk=self.request.user.endereco_id).first()})
    
class AddressRemoveView(SuccessMessageMixin, DeleteView):
    """
    View para remover um endereço do perfil do usuário logado. 
    A view exibe uma confirmação antes de excluir o endereço e, 
    após a remoção bem-sucedida, exibe uma mensagem de sucesso.
    """
    template_name = "address/excluir/removeAddress.html"
    model = Endereco
    context_object_name = 'endereco'
    success_message = "Endereço removido com sucesso."

    def get_success_url(self):
        """
        Retorna a URL de sucesso após a remoção do endereço. 
        O usuário será redirecionado para a página de edição do perfil.
        """
        user_id = self.kwargs['id'] 
        return reverse_lazy('editProfile', kwargs={'id': user_id})
    
    def get_object(self, queryset=None):
        """
        Sobrescreve o método para garantir que apenas endereços pertencentes ao usuário logado 
        possam ser removidos. Caso o endereço não exista ou não pertença ao usuário, 
        uma exceção Http404 é lançada.
        """
        endereco_id = self.kwargs.get('endereco_id')  
        try:
            endereco = Endereco.objects.get(pk=endereco_id, user=self.request.user)
        except Endereco.DoesNotExist:
            raise Http404("Endereço não encontrado ou não autorizado.")
        return endereco

    def get_context_data(self, **kwargs):
        """
        Adiciona o endereço atual ao contexto para exibição no template. 
        Isso permite que o usuário veja as informações do endereço antes de confirmar a remoção.
        """
        context = super().get_context_data(**kwargs)
        context['address'] = self.get_object()
        return context

    def delete(self, request, *args, **kwargs):
        """
        Sobrescreve o método delete para adicionar uma mensagem de sucesso após a remoção do endereço.
        Após a exclusão do endereço, o usuário é redirecionado com a mensagem de sucesso.
        """
        response = super().delete(request.user.endereco, *args, **kwargs)
        messages.success(self.request, self.success_message)
        return response
