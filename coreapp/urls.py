from django.urls import path
from django.contrib.auth.models import User
from django.contrib.auth import views as contrib_views
from django.conf.urls import include
from pblacore import urls as pblacoreurls
from . import views, urls_api

urlpatterns = [
    path('home/professor/dash', views.ProfessorDash.as_view(), name='professor_dash'),
    path('home/professor/turmas/', views.TurmasListView.as_view(), name='professor_turmas'),
    path('home/estudante', views.Estudante.as_view(), name='estudante'),
    path('home/professor/turmas/<str:tag_turma>/equipes', views.EquipeListView.as_view(), name='professor_equipes')
]

urlpatterns += [
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('home/adm', views.MyAdmView.as_view(), name='adm'),
]

urlpatterns += urls_api.urlpatterns