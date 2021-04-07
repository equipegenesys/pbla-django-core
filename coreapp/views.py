from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import views as contrib_views
from django.urls import reverse
from django.template import loader
from django.views.generic import TemplateView
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from .models import Turma
from .serializers import UserSerializer, GroupSerializer, TurmaSerializer
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class CustomLoginView(contrib_views.LoginView):

    def get_success_url(self):
        group_list = self.request.user.groups.values_list('name', flat=True)
        group_list = list(group_list)
        if 'professores' in group_list:
            return reverse("professor")
        elif 'estudantes' in group_list:
            return reverse("estudante")
        else:
            if self.request.user.is_staff:
                print("é admin")
                return reverse("adm")


class Professor(PermissionRequiredMixin, TemplateView):
    template_name = "vis/dash.html"
    permission_required = ('coreapp.view_dash')


class Estudante(PermissionRequiredMixin, TemplateView):
    template_name = "home/estudante.html"
    permission_required = ('coreapp.view_myestudante')

class MyAdmView(PermissionRequiredMixin, TemplateView):
    template_name = "home/adm.html"
    permission_required = ('coreapp.view_myadm')

def get_turmas_from_user(user_id: int):
    turmas_for_user = Turma.user.through.objects.filter(user_id=user_id)
    for turma in turmas_for_user:
        print(turma)
        return {'status': 'OK'}

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
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request, *args, **kwargs):
        user_id = kwargs.get('id')
        queryset = Turma.objects.filter(user__id=user_id)
        serializer = TurmaSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



# @login_required
# def admin_redirect(request):
#     return HttpResponse('Você é administrador. Acesse <a href="https://analytics.pbl.tec.br/admin/">aqui</a> o portal de administração.')

# @login_required
# def professor(request):
#     template = loader.get_template('vis/dash.html')
#     return HttpResponse(template.render())
    # return HttpResponse("Você está na home do professor.")

# @permission_required("coreapp.view_myestudante")
# def estudante(request):
#     return HttpResponse("Você está na home do estudante.")
