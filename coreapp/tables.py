# tutorial/tables.py
import django_tables2 as tables
from django.contrib.auth.models import User, Group
from . import models
from django_tables2.utils import A 

# from .models import ExtendedUser


class InstituicaoTable(tables.Table):
    # first_name = tables.LinkColumn('pessoas', empty_values=())  # not in meta

    class Meta:
        model = models.Instituicao
        template_name = "django_tables2/bootstrap4.html"
        fields = ("id", "name", )
        attrs = {"class": "table table-hover"}
        row_attrs = {
            'class': 'hover-class'
        }
    
    # def get_pk(self, pk: int):
    #     return pk

class CursoTable(tables.Table):
    # first_name = tables.LinkColumn('pessoas', empty_values=())  # not in meta

    class Meta:
        model = models.Curso
        template_name = "django_tables2/bootstrap4.html"
        fields = ("id", "instituicao", "name", "nivel" )
        attrs = {"class": "table table-hover"}
        row_attrs = {
            # 'onclick': "window.location='https://analytics.pbl.tec.br/adm/pessoas'",
            'class': 'hover-class'
        }

class TurmaTable(tables.Table):
    # first_name = tables.LinkColumn('pessoas', empty_values=())  # not in meta

    class Meta:
        model = models.Turma
        template_name = "django_tables2/bootstrap4.html"
        fields = ("id", "disciplina", "ano", "semestre", "tag_turma")
        attrs = {"class": "table table-hover"}
        row_attrs = {
            # 'onclick': "window.location='https://analytics.pbl.tec.br/adm/pessoas'",
            'class': 'hover-class'
        }

class TurmaTableEstudante(tables.Table):
    # first_name = tables.LinkColumn('pessoas', empty_values=())  # not in meta

    class Meta:
        model = models.Turma
        template_name = "django_tables2/bootstrap4.html"
        fields = ("id", "disciplina", "ano", "semestre", "tag_turma")
        # attrs = {"class": "table table-hover"}
        # row_attrs = {
            # 'onclick': "window.location='https://analytics.pbl.tec.br/adm/pessoas'",
            # 'class': 'hover-class'
        # }

class DisciplinaTable(tables.Table):
    # first_name = tables.LinkColumn('pessoas', empty_values=())  # not in meta

    class Meta:
        model = models.Disciplina
        template_name = "django_tables2/bootstrap4.html"
        fields = ("id", "curso", "name", "tag_disciplina")
        attrs = {"class": "table table-hover"}
        row_attrs = {
            # 'onclick': "window.location='https://analytics.pbl.tec.br/adm/pessoas'",
            'class': 'hover-class'
        }

class EquipeTable(tables.Table):
    # first_name = tables.LinkColumn('pessoas', empty_values=())  # not in meta

    class Meta:
        model = models.Equipe
        template_name = "django_tables2/bootstrap4.html"
        fields = ("id", "name", "tag_equipe", "user")
        attrs = {"class": "table table-hover"}
        row_attrs = {
            # 'onclick': "window.location='https://analytics.pbl.tec.br/adm/pessoas'",
            'class': 'hover-class'
        }

class PersonTable(tables.Table):
    # first_name = tables.LinkColumn('pessoas', empty_values=())  # not in meta

    class Meta:
        model = models.Pessoa
        template_name = "django_tables2/bootstrap4.html"
        fields = ("id", "username", "first_name", "last_name", "email", "groups")
        attrs = {"class": "table table-hover"}
        row_attrs = {
            # 'onclick': "window.location='https://analytics.pbl.tec.br/adm/pessoas'",
            'class': 'hover-class'
        }

class IntegracaoInstiTable(tables.Table):
    # first_name = tables.LinkColumn('pessoas', empty_values=())  # not in meta

    status_column = tables.Column(
        accessor='integ_status',
        verbose_name='Status',
        attrs={
            "td": {
                # "style": "color: %s" % lambda value: 'green' if value == 'Conectado' else 'green'
                "style": lambda value: "color: green; font-weight: bold" if value == 'Conectado' else "color: red; font-weight: bold"
                }
            }
        )

    instituicao_id_column = tables.Column(accessor='get_insti_id',
         verbose_name='ID da instituição', visible=True)

    integracao_id_column = tables.Column(accessor='get_integ_id',
         verbose_name='ID da integração', visible=True)

    class Meta:
        model = models.InstituicaoIntegBridge
        template_name = "django_tables2/bootstrap4.html"
        fields = ("instituicao", "instituicao_id_column", "integracao", "integracao_id_column", "status_column")
        attrs = {"class": "table table-hover"}
        row_attrs = {
            # 'onclick': "window.location='https://analytics.pbl.tec.br/adm/pessoas'",
            'class': 'hover-class'
        }

class IntegracaoUserTable(tables.Table):
    # first_name = tables.LinkColumn('pessoas', empty_values=())  # not in meta

    status_column = tables.Column(
        accessor='integ_status',
        verbose_name='Status',
        attrs={
            "td": {
                # "style": "color: %s" % lambda value: 'green' if value == 'Conectado' else 'green'
                "style": lambda value: "color: green; font-weight: bold" if value == 'Conectado' else "color: red; font-weight: bold"
                }
            }
        )

    instituicao_id_column = tables.Column(accessor='get_pessoa_id',
         verbose_name='ID do usuário', visible=True)

    integracao_id_column = tables.Column(accessor='get_integ_id',
         verbose_name='ID da integração', visible=True)

    class Meta:
        model = models.UserIntegBridge
        template_name = "django_tables2/bootstrap4.html"
        fields = ("pessoa", "instituicao_id_column", "integracao", "integracao_id_column", "status_column")
        attrs = {"class": "table table-hover"}
        row_attrs = {
            # 'onclick': "window.location='https://analytics.pbl.tec.br/adm/pessoas'",
            'class': 'hover-class'
        }