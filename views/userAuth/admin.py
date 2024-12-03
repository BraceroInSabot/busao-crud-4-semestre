from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

class Admin(UserAdmin):
    model = get_user_model()

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('telefone', 'usuario')}),
    )

    # Atualiza as colunas exibidas na lista de usuários
    list_display = ['usuario', 'email', 'nome', 'is_staff']
    search_fields = ['usuario', 'email', 'nome']

    ordering = ['usuario']

admin.site.register(get_user_model(), Admin)