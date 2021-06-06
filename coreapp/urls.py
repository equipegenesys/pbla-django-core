from django.urls import path
# from django.contrib.auth.models import User
# from django.contrib.auth import views as contrib_views
# from django.conf.urls import include
# from pblacore import urls as pblacoreurls
from . import views, urls_api

urlpatterns = [
    # path('home/professor/dash', views.ProfessorDash.as_view(), name='professor_dash'),
    path('professor/turmas/', views.TurmasListView.as_view(), name='professor_turmas'),
    path('estudante/integra', views.Estudante.as_view(), name='integra'),
    path('estudante/disciplinas', views.TurmasEstudante.as_view(), name='disciplinas'),
    path('professor/turmas/<str:tag_turma>/equipes/', views.EquipeListView.as_view(), name='professor_equipes'),
    path('professor/turmas/<str:tag_turma>/equipes/<str:tag_equipe>/', views.ProfessorDash.as_view(), name='professor_dash'),
    path('professor/update/turmas/<str:tag_turma>/equipes/<str:tag_equipe>/', views.UpdateDataView.as_view(), name='update_data')
]

urlpatterns += [
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', views.CustomLogoutView.as_view(), name='logout'),
    # path('home/adm', views.MyAdmView.as_view(), name='adm'),
]

urlpatterns += urls_api.urlpatterns