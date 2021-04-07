from django.contrib import admin
from . import models

class TurmaeAdmin(admin.ModelAdmin):
    fields = ['disciplina', 'ano', 'semestre', 'user', 'tag_turma']
    readonly_fields = ['tag_turma']

    def get_readonly_fields(self, request, obj=None):
        if obj: # when editing an object
            return ['tag_turma']
        return self.readonly_fields

    # def tag_turma(self, obj):
    #     return '*** CLASSIFIED *** {}'.format(obj.tag_turma)


class EquipeAdmin(admin.ModelAdmin):
    # readonly_fields = ('get_c',)
    fields = ['name', 'turma', 'user', 'tag_equipe']
    readonly_fields = ['tag_equipe']
    #     return obj.a + obj.b

    def get_readonly_fields(self, request, obj=None):
        
        if obj: # when editing an object
            print("obj é .......... :",obj)
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

admin.site.register(models.Instituicao)
admin.site.register(models.Curso)
admin.site.register(models.Disciplina, DisciplinaAdmin)
admin.site.register(models.Turma, TurmaeAdmin)
admin.site.register(models.Equipe, EquipeAdmin)