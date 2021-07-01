from . import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
    
admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # form = MyUserChangeForm
    list_display = ('first_name', 'last_name', 'id', 'username', 'email', 'is_staff')
    fieldsets = (
    (None, {'fields': ('id',)}),
    ) + UserAdmin.fieldsets
    readonly_fields = ('id',)
    # inlines = [TurmasInline]
    # inlines = (TurmasInline, )


class TurmaeAdmin(admin.ModelAdmin):
    fields = ['disciplina', 'ano', 'semestre', 'user', 'tag_turma']
    # list_display = ('user')
    readonly_fields = ['tag_turma']

    def get_readonly_fields(self, request, obj=None):
        if obj: # when editing an object
            return ['tag_turma']
        return self.readonly_fields


class EquipeAdmin(admin.ModelAdmin):
    # readonly_fields = ('get_c',)
    fields = ['name', 'turma', 'user', 'tag_equipe']
    readonly_fields = ['tag_equipe']
    #     return obj.a + obj.b

    def get_readonly_fields(self, request, obj=None):
        
        if obj: # when editing an object
            # print("obj é .......... :",obj)
            return ['tag_equipe']
        return self.readonly_fields


class DisciplinaAdmin(admin.ModelAdmin):
    fields = ['curso', 'name', 'tag_disciplina']
    readonly_fields = ['tag_disciplina']
    
    # def tag_disciplina(self, obj):
    #     return '*** CLASSIFIED *** {}'.format(obj.tag_disciplina)

    def get_readonly_fields(self, request, obj=None):
        if obj: # when editing an object
            return ['tag_disciplina']
        return self.readonly_fields


class InstituicaoInline(admin.TabularInline):
    model = models.Integracao.instituicao.through
    extra = 0
    max_num = 0
    readonly_fields = ['instituicao','first_created','is_active_update_date','is_active']
    can_delete = False

class EquipeInline(admin.TabularInline):
    model = models.Integracao.equipe.through
    extra = 0
    max_num = 0
    readonly_fields = ['equipe','first_created','is_active_update_date','is_active']
    can_delete = False

class PessoaInline(admin.TabularInline):
    model = models.Integracao.pessoa.through
    extra = 0
    max_num = 0
    readonly_fields = ['pessoa','first_created','is_active_update_date','is_active']
    can_delete = False

class IntegracaoAdmin(admin.ModelAdmin):
    fields = ['name', 'root_endpoint']
    list_display = ('name', 'root_endpoint')
    inlines = [
        InstituicaoInline,
        EquipeInline,
        PessoaInline
    ]


admin.site.register(models.Instituicao)
admin.site.register(models.Curso)
admin.site.register(models.Disciplina, DisciplinaAdmin)
admin.site.register(models.Turma, TurmaeAdmin)
admin.site.register(models.Equipe, EquipeAdmin)
admin.site.register(models.Integracao, IntegracaoAdmin)