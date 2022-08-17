from django.contrib import admin
from .models import Contato, Categoria


class ContatoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'sobrenome', 'telefone', 'email', 'data_criacao', 'categoria')
    list_display_links = ('id', 'nome', 'sobrenome')
    list_filter = ('categoria',)
    search_fields = ('nome', 'sobrenome', 'telefone', 'email', 'descricao')
    list_per_page = 10
    list_max_show_all = 10
    list_select_related = ('categoria',)
    date_hierarchy = 'data_criacao'
    ordering = ('-data_criacao',)
    fieldsets = (
        (None, {
            'fields': ('nome', 'sobrenome', 'telefone', 'email', 'descricao', 'categoria')
        }),
    )


admin.site.register(Contato, ContatoAdmin)
admin.site.register(Categoria)
