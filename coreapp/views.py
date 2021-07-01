import json
# from django.db.models.query_utils import Q
from django.shortcuts import redirect, render
# from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import views as contrib_views
# from django.contrib.auth.models import User as BuiltInUser
from django.contrib.auth import logout
from django.urls import reverse, reverse_lazy
# from django.template import loader
from django import template
from django.core import serializers as django_serializer
from django.http import HttpResponseRedirect


from django_tables2 import SingleTableView
from . import tables, forms

from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
# from django.views.generic.list import MultipleObjectMixin
# from django.template.response import TemplateResponse

# from django.contrib.auth.decorators import permission_required
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User, Group

# from rest_framework import viewsets
from rest_framework import permissions
# from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . import gateway
from . import serializers
from .models import Turma, TurmasClass, TurmaEquipe, Equipe, Disciplina, Instituicao, Curso, Pessoa
from .models import InstituicaoIntegBridge, UserIntegBridge
from django.db.models import Q
import pdb

from coreapp import models

# from multiprocessing import Pool
# from threading import Thread

# from asgiref.sync import sync_to_async

# pool = Pool(4)

register = template.Library()

class CustomLoginView(contrib_views.LoginView):

    form_class = forms.UserLoginForm

    def get_success_url(self):
        group_list = self.request.user.groups.values_list('name', flat=True)
        group_list = list(group_list)
        if 'professores' in group_list:
            return reverse("turmas")
        elif 'estudantes' in group_list:
            return reverse("integra")
        else:
            if self.request.user.is_staff:
                print("é admin")
                return reverse("adm")

class CustomLogoutView(contrib_views.LogoutView):
    def get_success_url(self):
        return reverse("login")

class UndefinedAttrs(PermissionRequiredMixin, TemplateView):
    template_name = "undefined.html"
    permission_required = ('coreapp.view_dash')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user_id = self.request.user.id
        turmas_queryset = Turma.objects.all().filter(user__id=current_user_id)
        minhas_turmas = []
        equipes_de_minhas_turmas = []        
        for turma in turmas_queryset:
            minhas_turmas.append(turma.__str__())
            equipes_queryset = Equipe.objects.all().filter(turma__tag_turma=turma.tag_turma)
            equipe_entry = equipes_queryset.all().values()[0]['name'] + " - " + equipes_queryset.all().values()[0]['tag_equipe']
            equipes_de_minhas_turmas.append(equipe_entry)                  
        equipes_de_minhas_turmas = set(equipes_de_minhas_turmas)
        # minhas_turmas_utf = json.dumps(minhas_turmas).encode('utf8')

        context['minhas_turmas'] = minhas_turmas
        context['minhas_equipes'] = equipes_de_minhas_turmas
        return context

class UpdateDataView(PermissionRequiredMixin, TemplateView):
    template_name = "vis/update.html"
    permission_required = ('coreapp.view_dash')

    def get_context_data(self, **kwargs):
        
        tag_turma = kwargs.get('tag_turma')
        tag_equipe = kwargs.get('tag_equipe')
        
        turma_equipe = TurmaEquipe()
        context = super().get_context_data(**kwargs)

        user_list = []
        users = User.objects.filter(equipe__tag_equipe=tag_equipe)
        for user in users:
            user_list.append(user.id)
        
        if tag_equipe:
            dados_turma = turma_equipe.get_name(tag_turma=tag_turma, tag_equipe=tag_equipe)
            context['nome_equipe'] = dados_turma['Equipe']
        else:
            dados_turma = turma_equipe.get_name(tag_turma=tag_turma)
        
        context['dash_view_url'] = f"https://analytics.pbl.tec.br/professor/turmas/{tag_turma}/equipes/{tag_equipe}/"
        context['nome_disciplina'] = dados_turma['Disciplina']
        context['semestre'] = dados_turma['Semestre']
        context['tag_turma'] = tag_turma
        context['tag_equipe'] = tag_equipe
        context['user_list'] = user_list
        context['user_count'] = len(user_list)
        return context

class AnalyticsDash(PermissionRequiredMixin, TemplateView):
    template_name = "vis/dash.html"
    permission_required = ('coreapp.view_dash')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tag_turma = kwargs.get('tag_turma')
        if tag_turma is None:
            tag_turma = 'all'
        print(tag_turma)
        tag_equipe = kwargs.get('tag_equipe')
        current_user_id = self.request.user.id

        turmas_queryset = Turma.objects.all().filter(user__id=current_user_id)

        minhas_turmas = []
        equipes_de_minhas_turmas = []        
        for turma in turmas_queryset:
            minhas_turmas.append(turma.__str__())
            equipes_queryset = Equipe.objects.all().filter(turma__tag_turma=turma.tag_turma)
            equipe_entry = equipes_queryset.all().values()[0]['name'] + " - " + equipes_queryset.all().values()[0]['tag_equipe']
            equipes_de_minhas_turmas.append(equipe_entry)                  
        equipes_de_minhas_turmas = set(equipes_de_minhas_turmas)
        minhas_turmas_utf = json.dumps(minhas_turmas).encode('utf8')

        turma_equipe = TurmaEquipe()

        if tag_equipe:
            dados_turma = turma_equipe.get_name(tag_turma=tag_turma, tag_equipe=tag_equipe)
            context['nome_equipe'] = dados_turma['Equipe']
        else:
            dados_turma = turma_equipe.get_name(tag_turma=tag_turma)
        
        context['filter_url'] = f"https://analytics.pbl.tec.br/dash/{tag_turma}/{tag_equipe}"
        context['nome_disciplina'] = dados_turma['Disciplina']
        context['subtitulo_metadados'] = f"Disciplina: {dados_turma['Disciplina']} | Semestre: {dados_turma['Semestre']}"
        context['semestre'] = dados_turma['Semestre']
        context['tag_turma'] = tag_turma
        context['tag_equipe'] = tag_equipe
        context['minhas_turmas_json'] = minhas_turmas_utf.decode()
        context['minhas_turmas'] = minhas_turmas
        context['minhas_equipes'] = equipes_de_minhas_turmas

        # context['updating_data'] = updating_data
        return context

class Estudante(PermissionRequiredMixin, TemplateView):
    template_name = "home/integra.html"
    permission_required = ('coreapp.view_myestudante')

    def get_context_data(self, **kwargs):
        queryset = Turma.objects.filter(user__id=self.request.user.id)
        current_user_id = self.request.user.id
        current_user_first_name = self.request.user.first_name
        if gateway.get_user_gdrive_status(current_user_id):
            g_drive_integ_status = 'Integrado'
        else:
            g_drive_integ_status = 'Não integrado'
        g_drive_integ_link = gateway.get_gdrive_integ_link(current_user_id)
        # print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", g_drive_integ_link)
        context = {
            'current_user_id': current_user_id,
            'current_user_first_name': current_user_first_name,
            'g_drive_integ_status': g_drive_integ_status,
            'g_drive_integ_link': g_drive_integ_link,
            'turmas_do_estudante': queryset,
        }
        return context
    
class TurmasEstudante(PermissionRequiredMixin, TemplateView):
    template_name = "home/disciplinas.html"
    permission_required = ('coreapp.view_myestudante')

    def get_context_data(self, **kwargs):
        queryset = Turma.objects.filter(user__id=self.request.user.id)
        current_user_id = self.request.user.id
        current_user_first_name = self.request.user.first_name
        if gateway.get_user_gdrive_status(current_user_id):
            g_drive_integ_status = 'Integrado'
        else:
            g_drive_integ_status = 'Não integrado'
        g_drive_integ_link = gateway.get_gdrive_integ_link(current_user_id)
        context = {
            'current_user_id': current_user_id,
            'current_user_first_name': current_user_first_name,
            'g_drive_integ_status': g_drive_integ_status,
            'g_drive_integ_link': g_drive_integ_link,
            'turmas_do_estudante': queryset,
        }
        return context

class TurmasListView(PermissionRequiredMixin, TemplateView):
    template_name = "home/turmas.html"
    permission_required = ('coreapp.view_dash')
    
    def get_context_data(self, **kwargs):
        queryset = Turma.objects.filter(user__id=self.request.user.id)      
        context = {
            'object_list': queryset,
            'object_count': queryset.count(),
        }
        return context

class EquipeListView(PermissionRequiredMixin, TemplateView):
    template_name = "home/equipes.html"
    permission_required = ('coreapp.view_dash')
    
    def get_context_data(self, **kwargs):
        tag_turma = kwargs.get('tag_turma')
        queryset = Equipe.objects.filter(turma=Turma.objects.get(tag_turma=tag_turma))
        turma_equipe = TurmaEquipe()
        dados_turma = turma_equipe.get_name(tag_turma=tag_turma)     
        context = {
            'object_list': queryset,
            'object_count': queryset.count(),
            'tag_turma': tag_turma,
            'nome_disciplina': dados_turma['Disciplina'],
            'semestre': dados_turma['Semestre'],
            'base_url': f'https://analytics.pbl.tec.br/professor/update/turmas/{tag_turma}/equipes/'
        }
        return context


class InstituicaoListView(PermissionRequiredMixin, SingleTableView):
    model = Instituicao
    permission_required = ('coreapp.view_dash')
    table_class = tables.InstituicaoTable
    template_name = 'tables.html'
    table_pagination = {
        "per_page": 8
    }
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Instituições'
        context['subpath'] = 'instituicoes'
        context['object_count'] = len(self.model.objects.values_list())
        return context
class InstituicaoDetalheView(PermissionRequiredMixin, DetailView):
    model = Instituicao
    permission_required = ('coreapp.view_dash')
    template_name = 'adm_detail.html'
    def get_object(self, queryset=None):
        return Instituicao.objects.get(pk=self.kwargs.get("pk"))    
    def get_context_data(self, **kwargs):
        # print(self.kwargs.get("pk"))
        context = super().get_context_data(**kwargs)
        context['title'] = 'Instituição'
        pk_str = str(self.kwargs.get("pk"))
        context['subpath_excluir'] = f"instituicoes/delete/{pk_str}"
        context['subpath_editar'] = f"instituicoes/edit/{pk_str}"        
        return context
class InstituicaoCreateView(PermissionRequiredMixin, CreateView):
    model = Instituicao
    permission_required = ('coreapp.view_dash')
    form_class = forms.InstituicaoForm
    def form_valid(self, form):
        return super().form_valid(form)
class InstituicaoDeleteView(PermissionRequiredMixin, DeleteView):
    model = Instituicao
    permission_required = ('coreapp.view_dash')
    success_url = reverse_lazy('instituicoes')
class InstituicaoUpdateView(PermissionRequiredMixin, UpdateView):
    model = Instituicao
    permission_required = ('coreapp.view_dash')
    form_class = forms.InstituicaoForm
    template_name_suffix = '_update_form'

    def get_success_url(self, **kwargs):
        pk = self.kwargs.get("pk")
        return reverse('insti-detalhe', kwargs={'pk': pk})


class CursoListView(PermissionRequiredMixin, SingleTableView):
    model = Curso
    permission_required = ('coreapp.view_dash')
    table_class = tables.CursoTable
    template_name = 'tables.html'
    table_pagination = {
        "per_page": 8
    }
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cursos'
        context['subpath'] = 'cursos'
        context['object_count'] = len(self.model.objects.values_list())
        return context
class CursoDetalheView(PermissionRequiredMixin, DetailView):
    model = Curso
    permission_required = ('coreapp.view_dash')
    template_name = 'adm_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Curso'
        pk_str = str(self.kwargs.get("pk"))
        context['subpath_excluir'] = f"cursos/delete/{pk_str}"
        context['subpath_editar'] = f"cursos/edit/{pk_str}"
        return context
class CursoCreateView(PermissionRequiredMixin, CreateView):
    model = Curso
    permission_required = ('coreapp.view_dash')
    form_class = forms.CursoForm
    # fields = ['instituicao', 'name', 'nivel']
    def form_valid(self, form):
        return super().form_valid(form)
class CursoDeleteView(PermissionRequiredMixin, DeleteView):
    model = Curso
    permission_required = ('coreapp.view_dash')
    success_url = reverse_lazy('cursos')
class CursoUpdateView(PermissionRequiredMixin, UpdateView):
    model = Curso
    permission_required = ('coreapp.view_dash')
    form_class = forms.CursoForm
    template_name_suffix = '_update_form'

    def get_success_url(self, **kwargs):
        pk = self.kwargs.get("pk")
        return reverse('curso-detalhe', kwargs={'pk': pk})


class DisciplinaListView(PermissionRequiredMixin, SingleTableView):
    model = Disciplina
    permission_required = ('coreapp.view_dash')
    table_class = tables.DisciplinaTable
    template_name = 'tables.html'
    table_pagination = {
        "per_page": 8
    }
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Disciplinas'
        context['subpath'] = 'disciplinas'
        context['object_count'] = len(self.model.objects.values_list())
        return context
class DisciplinaDetalheView(PermissionRequiredMixin, DetailView):
    model = Disciplina
    permission_required = ('coreapp.view_dash')
    template_name = 'adm_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Disciplina'
        pk_str = str(self.kwargs.get("pk"))
        context['subpath_excluir'] = f"disciplinas/delete/{pk_str}"
        context['subpath_editar'] = f"disciplinas/edit/{pk_str}"
        return context
class DisciplinaCreateView(PermissionRequiredMixin, CreateView):
    model = Disciplina
    permission_required = ('coreapp.view_dash')
    form_class = forms.DisciplinaForm
    def form_valid(self, form):
        return super().form_valid(form)
class DisciplinaDeleteView(PermissionRequiredMixin, DeleteView):
    model = Disciplina
    permission_required = ('coreapp.view_dash')
    success_url = reverse_lazy('disciplinas')
class DisciplinaUpdateView(PermissionRequiredMixin, UpdateView):
    model = Disciplina
    permission_required = ('coreapp.view_dash')
    form_class = forms.DisciplinaForm
    template_name_suffix = '_update_form'

    def get_success_url(self, **kwargs):
        pk = self.kwargs.get("pk")
        return reverse('disci-detalhe', kwargs={'pk': pk})


class TurmaListView(PermissionRequiredMixin, SingleTableView):
    model = Turma
    permission_required = ('coreapp.view_dash')
    table_class = tables.TurmaTable
    template_name = 'tables.html'
    table_pagination = {
        "per_page": 8
    }
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Turmas'
        context['subpath'] = 'turmas'
        context['object_count'] = len(self.model.objects.values_list())
        return context
class TurmaDetalheView(PermissionRequiredMixin, DetailView):
    model = Turma
    permission_required = ('coreapp.view_dash')
    template_name = 'adm_detail.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Turma'
        pk_str = str(self.kwargs.get("pk"))
        context['subpath_excluir'] = f"turmas/delete/{pk_str}"
        context['subpath_editar'] = f"turmas/edit/{pk_str}"
        return context
class TurmaCreateView(PermissionRequiredMixin, CreateView):
    model = Turma
    permission_required = ('coreapp.view_dash')
    form_class = forms.TurmaForm
    def form_valid(self, form):
        return super().form_valid(form)
class TurmaDeleteView(PermissionRequiredMixin, DeleteView):
    model = Turma
    permission_required = ('coreapp.view_dash')
    success_url = reverse_lazy('turmas')
class TurmaUpdateView(PermissionRequiredMixin, UpdateView):
    model = Turma
    permission_required = ('coreapp.view_dash')
    form_class = forms.TurmaForm
    template_name_suffix = '_update_form'

    def get_success_url(self, **kwargs):
        pk = self.kwargs.get("pk")
        return reverse('turma-detalhe', kwargs={'pk': pk})

class TurmaListViewEstudante(PermissionRequiredMixin, SingleTableView):
    model = Turma
    permission_required = ('coreapp.view_myestudante')
    table_class = tables.TurmaTableEstudante
    template_name = 'tables_estudante.html'
    table_pagination = {
        "per_page": 8
    }
    def get_queryset(self):
        return Turma.objects.filter(user__id=self.request.user.id)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Minhas disciplinas'
        context['subpath'] = 'turmas'
        context['object_count'] = len(self.model.objects.values_list())
        return context

class EquipeListView(PermissionRequiredMixin, SingleTableView):
    model = Equipe
    permission_required = ('coreapp.view_dash')
    table_class = tables.EquipeTable
    template_name = 'tables.html'
    table_pagination = {
        "per_page": 8
    }
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Equipes'
        context['subpath'] = 'equipes'
        context['object_count'] = len(self.model.objects.values_list())
        return context
class EquipeDetalheView(PermissionRequiredMixin, DetailView):
    model = Equipe
    permission_required = ('coreapp.view_dash')
    template_name = 'adm_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Equipe'
        pk_str = str(self.kwargs.get("pk"))
        context['subpath_excluir'] = f"equipes/delete/{pk_str}"
        context['subpath_editar'] = f"equipes/edit/{pk_str}"
        return context
class EquipeCreateView(PermissionRequiredMixin, CreateView):
    model = Equipe
    permission_required = ('coreapp.view_dash')
    form_class = forms.EquipeForm
    def form_valid(self, form):
        return super().form_valid(form)
class EquipeDeleteView(PermissionRequiredMixin, DeleteView):
    model = Equipe
    permission_required = ('coreapp.view_dash')
    success_url = reverse_lazy('equipes')
class EquipeUpdateView(PermissionRequiredMixin, UpdateView):
    model = Equipe
    permission_required = ('coreapp.view_dash')
    form_class = forms.EquipeForm
    template_name_suffix = '_update_form'

    def get_success_url(self, **kwargs):
        pk = self.kwargs.get("pk")
        return reverse('equipe-detalhe', kwargs={'pk': pk})

class PersonListView(PermissionRequiredMixin, SingleTableView):
    model = Pessoa
    permission_required = ('coreapp.view_dash')
    table_class = tables.PersonTable
    table_data = Pessoa.objects.filter(Q(is_staff=False) & Q(is_superuser=False))
    template_name = 'tables.html'
    table_pagination = {
        "per_page": 8
    }
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Pessoas'
        context['subpath'] = 'pessoas'
        context['object_count'] = len(self.model.objects.values_list())
        return context
class PessoaDetalheView(PermissionRequiredMixin, DetailView):
    model = Pessoa
    permission_required = ('coreapp.view_dash')
    template_name = 'adm_detail.html'    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Pessoa'
        pk_str = str(self.kwargs.get("pk"))
        context['subpath_excluir'] = f"pessoas/delete/{pk_str}"
        context['subpath_editar'] = f"pessoas/edit/{pk_str}"
        return context
class PessoaCreateView(PermissionRequiredMixin, CreateView):
    model = Pessoa
    permission_required = ('coreapp.view_dash')
    form_class = forms.PessoaForm
    def form_valid(self, form):
        return super().form_valid(form)
class PessoaUpdateView(PermissionRequiredMixin, UpdateView):
    model = Pessoa
    permission_required = ('coreapp.view_dash')
    form_class = forms.PessoaForm
    template_name_suffix = '_update_form'

    def get_success_url(self, **kwargs):
        pk = self.kwargs.get("pk")
        return reverse('pessoa-detalhe', kwargs={'pk': pk})
class PessoaDeleteView(PermissionRequiredMixin, DeleteView):
    model = Pessoa
    permission_required = ('coreapp.view_dash')
    success_url = reverse_lazy('pessoas')

    def delete(self, *args, **kwargs):
        if self.model.objects.get(pk=kwargs.get("pk")).is_staff or self.model.objects.get(pk=kwargs.get("pk")).is_superuser:
            print("opa")
            raise Exception('Você não pode apagar usuários administradores.')  # or you can throw your custom exception here.
        return super(PessoaDeleteView, self).delete(*args, **kwargs)


class TurmaUserView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        myClass = TurmasClass()
        myClass.user_id = user_id
        # print("                   ", myClass.user_id)
        result = myClass.get_turmas(user_id)
        response = Response(result, status=status.HTTP_200_OK)
        return response

class UsersEquipeView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, **kwargs):
        tag_equipe = kwargs.get('tag_equipe')
        queryset = Equipe.objects.get(tag_equipe=tag_equipe)
        serializer = serializers.IntegrantesSerializer(queryset)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        return response

class RealNames(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, **kwargs):
        tag_turma = kwargs.get('tag_turma')
        tag_equipe = kwargs.get('tag_equipe')

        turma_equipe = TurmaEquipe()
        
        if tag_turma != None and tag_equipe == None:
            result = turma_equipe.get_name(tag_turma=tag_turma)
        elif tag_turma != None and tag_equipe != None:
            result = turma_equipe.get_name(tag_turma=tag_turma, tag_equipe=tag_equipe)

        response = Response(result, status=status.HTTP_200_OK)
        
        return response

class IntegApi(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):

        # print(self.request.path[16:-1])

        # user_id = kwargs.get('id')
        # equipe = kwargs.get('tag_equipe')
        # intituicao = kwargs.get('inst_pk')
        # activated = kwargs.get('activated')

        if self.request.path[16:-1] == 'pessoa':
            serializer = serializers.UserIntegSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif self.request.path[16:-1] == 'equipe':
            serializer = serializers.EquipeIntegSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif self.request.path[16:-1] == 'instituicao':
            serializer = serializers.InstituicaoIntegSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response('nenhum das opções foi fornecida', status=status.HTTP_200_OK)


class IntegracaoInstiListView(PermissionRequiredMixin, SingleTableView):
    model = InstituicaoIntegBridge
    permission_required = ('coreapp.view_dash')
    table_class = tables.IntegracaoInstiTable
    table_data = InstituicaoIntegBridge.objects.filter(Q(is_active=True))
    template_name = 'tables_integ.html'
    table_pagination = {
        "per_page": 8
    }
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Integrações das instituições'
        context['subpath'] = 'integ'
        context['object_count'] = len(self.model.objects.values_list())
        return context

class IntegracaoInstiUpdateView(PermissionRequiredMixin, FormView):

    permission_required = ('coreapp.view_dash')
    template_name = 'discord_token_form.html'
    form_class = forms.IntegracaoInstiForm
    success_url = 'https://analytics.pbl.tec.br/adm/instituicoes/integ'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        insti_id = str(self.kwargs.get("insti_id"))
        integ_id = str(self.kwargs.get("integ_id"))
        context['insti_id'] = insti_id
        context['integ_id'] = integ_id
        # print(insti_id, integ_id)
        return context

    def form_valid(self, form):

        print(form.cleaned_data['discord_token'])
        gateway.post_discord_token(form.cleaned_data['discord_token'])
        return super().form_valid(form)

class IntegracaoUserListView(PermissionRequiredMixin, SingleTableView):
    model = UserIntegBridge
    permission_required = ('coreapp.view_myestudante')
    table_class = tables.IntegracaoUserTable
    # table_data = UserIntegBridge.objects.filter(Q(is_active=True))
    template_name = 'tables_integ_estudante.html'
    table_pagination = {
        "per_page": 8
    }
    def get_queryset(self):
        return UserIntegBridge.objects.filter(pessoa__id=self.request.user.id)

    def get_context_data(self, **kwargs):
        g_drive_integ_link = gateway.get_gdrive_integ_link(self.request.user.id)

        context = super().get_context_data(**kwargs)
        context['title'] = 'Minhas integrações'
        context['subpath'] = 'integ'
        context['object_count'] = len(self.model.objects.values_list())
        context['g_drive_integ_link'] = g_drive_integ_link
        context['current_user_id'] = self.request.user.id
        return context

def create_gdrive_integ(request):
    models.UserIntegBridge.objects.create(
        pessoa = models.Pessoa.objects.get(pk=request.user.id), 
        integracao = models.Integracao.objects.get(pk=1), 
        is_active = True)
    return HttpResponseRedirect('https://analytics.pbl.tec.br/estudante/integra')