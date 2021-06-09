from django.db.models.query_utils import Q
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import views as contrib_views
# from django.contrib.auth.models import User as BuiltInUser
from django.contrib.auth import logout
from django.urls import reverse
from django.template import loader
from django import template
from django.core import serializers as django_serializer

from django_tables2 import SingleTableView
from . import tables

from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.list import MultipleObjectMixin
from django.template.response import TemplateResponse

# from django.contrib.auth.decorators import permission_required
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User, Group

from rest_framework import viewsets
from rest_framework import permissions
# from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . import gateway
from .serializers import UserSerializer, GroupSerializer, TurmaSerializer, IntegrantesSerializer
from .models import Turma, TurmasClass, TurmaEquipe, Equipe, Disciplina, Instituicao, Curso, Pessoa

# from multiprocessing import Pool
from threading import Thread

# from asgiref.sync import sync_to_async

# pool = Pool(4)

register = template.Library()

class CustomLoginView(contrib_views.LoginView):

    def get_success_url(self):
        group_list = self.request.user.groups.values_list('name', flat=True)
        group_list = list(group_list)
        if 'professores' in group_list:
            return reverse("professor_turmas")
        elif 'estudantes' in group_list:
            return reverse("integra")
        else:
            if self.request.user.is_staff:
                print("é admin")
                return reverse("adm")

class CustomLogoutView(contrib_views.LogoutView):
    def get_success_url(self):
        return reverse("login")



# async def UpdateDataView(request, tag_turma, tag_equipe):
#     template_name = 'vis/update.html'
    
#     # print(tag_turma, tag_equipe)
    
#     user_list = []
#     # users = User.objects.filter(equipe__tag_equipe=tag_equipe)

#     users = await sync_to_async(list)(User.objects.filter(equipe__tag_equipe=tag_equipe))
#     # print(users)
    
#     for user in users:
#         user_list.append(user.id)
#     print("           user_list:", user_list)
    
#     results  = await asyncio.gather(gateway.update_gdrive_records(user_list))

#     print(results)
    
#     return render(request, template_name)




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
        print(context)
        return context


class ProfessorDash(PermissionRequiredMixin, TemplateView):
    template_name = "vis/dash.html"
    permission_required = ('coreapp.view_dash')
    # print(django.VERSION)

    def get_context_data(self, **kwargs):

        # tag_turma = self.request.GET.get('turma')
        # tag_equipe = self.request.GET.get('equipe')
        
        tag_turma = kwargs.get('tag_turma')
        tag_equipe = kwargs.get('tag_equipe')



        
        # users = User.objects.filter(equipe__tag_equipe=tag_equipe)
        # t = Thread(target=gateway.update_gdrive_records, args=(users, ))
        # t.start()
        # print("this will be printed immediately")

        # if t.is_alive():
        #     updating_data = True
        #     print(updating_data)
        # else:
        #     updating_data = False
        #     print(updating_data)
            


        turma_equipe = TurmaEquipe()
        context = super().get_context_data(**kwargs)
        
        if tag_equipe:
            dados_turma = turma_equipe.get_name(tag_turma=tag_turma, tag_equipe=tag_equipe)
            context['nome_equipe'] = dados_turma['Equipe']
        else:
            dados_turma = turma_equipe.get_name(tag_turma=tag_turma)
        
        context['filter_url'] = f"https://analytics.pbl.tec.br/dash/{tag_turma}/{tag_equipe}"
        context['nome_disciplina'] = dados_turma['Disciplina']
        context['semestre'] = dados_turma['Semestre']
        context['tag_turma'] = tag_turma
        context['tag_equipe'] = tag_equipe
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



class InstituicaoListView(SingleTableView):
    model = Instituicao
    table_class = tables.InstituicaoTable
    template_name = 'tables.html'
    table_pagination = {
        "per_page": 8
    }
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Instituições'
        return context
class InstituicaoDetalheView(DetailView):
    model = Instituicao
    template_name = 'adm_detail.html'

    def get_object(self, queryset=None):
        print(self.kwargs.get("pk"))
        print(type(self.kwargs.get("pk")))
        return Instituicao.objects.get(pk=self.kwargs.get("pk"))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Instituição"'
        return context



class CursoListView(SingleTableView):
    model = Curso
    table_class = tables.CursoTable
    template_name = 'tables.html'
    table_pagination = {
        "per_page": 8
    }
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cursos'
        return context
class CursoDetalheView(DetailView):
    model = Curso
    template_name = 'adm_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Curso'
        return context


class DisciplinaListView(SingleTableView):
    model = Disciplina
    table_class = tables.DisciplinaTable
    template_name = 'tables.html'
    table_pagination = {
        "per_page": 8
    }
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Disciplinas'
        return context
class DisciplinaDetalheView(DetailView):
    model = Disciplina
    template_name = 'adm_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Disciplina'
        return context



class TurmaListView(SingleTableView):
    model = Turma
    table_class = tables.TurmaTable
    template_name = 'tables.html'
    table_pagination = {
        "per_page": 8
    }
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Turmas'
        return context
class TurmaDetalheView(DetailView):
    model = Turma
    template_name = 'adm_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Turma'
        return context


class EquipeListView(SingleTableView):
    model = Equipe
    table_class = tables.EquipeTable
    template_name = 'tables.html'
    table_pagination = {
        "per_page": 8
    }
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Equipes'
        return context
class EquipeDetalheView(DetailView):
    model = Equipe
    template_name = 'adm_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Equipe'
        return context



class PersonListView(SingleTableView):
    model = Pessoa
    table_class = tables.PersonTable
    template_name = 'tables.html'
    table_pagination = {
        "per_page": 8
    }
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Pessoas'
        return context
class PessoaDetalheView(DetailView):
    model = Pessoa
    template_name = 'adm_detail.html'

    # def get_object(self, queryset=None):
    #     # print(self.kwargs.get("pk"))
    #     # print(type(self.kwargs.get("pk")))
    #     return self.model.objects.get(pk=self.kwargs.get("pk"))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Pessoa'
        return context









class MyAdmView(PermissionRequiredMixin, TemplateView):
    template_name = "home/adm.html"
    permission_required = ('coreapp.view_myadm')


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class TurmaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows turmas to be viewed or edited.
    """
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer
    permission_classes = [permissions.IsAuthenticated]


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
        serializer = IntegrantesSerializer(queryset)
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


    
    
