from django.urls import path, include
from . import views, urls_api

urlpatterns = [
    path('professor/turmas/', views.TurmasListView.as_view(), name='professor_turmas'),
    path('estudante/integra', views.Estudante.as_view(), name='integra'),
    path('estudante/disciplinas', views.TurmasEstudante.as_view(), name='disciplinas'),
    path('professor/turmas/<str:tag_turma>/equipes/<str:tag_equipe>/', views.ProfessorDash.as_view(), name='professor_dash'),
    # path('professor/update/turmas/<str:tag_turma>/equipes/<str:tag_equipe>/', views.UpdateDataView.as_view(), name='update_data'),

    path("adm/instituicoes", views.InstituicaoListView.as_view(), name='instituicoes'),
    path("adm/cursos", views.CursoListView.as_view(), name='cursos'),
    path("adm/disciplinas", views.DisciplinaListView.as_view(), name='disciplinas'),
    path("adm/turmas", views.TurmaListView.as_view(), name='turmas'),
    path("adm/equipes", views.EquipeListView.as_view(), name='equipes'),
    path("adm/pessoas", views.PersonListView.as_view(), name='pessoas'),

    path('adm/instituicoes/<int:pk>', views.InstituicaoDetalheView.as_view(), name='insti-detalhe'),
    path('adm/cursos/<int:pk>', views.CursoDetalheView.as_view(), name='curso-detalhe'),
    path('adm/disciplinas/<int:pk>', views.DisciplinaDetalheView.as_view(), name='disci-detalhe'),
    path('adm/turmas/<int:pk>', views.TurmaDetalheView.as_view(), name='turma-detalhe'),
    path('adm/equipes/<int:pk>', views.EquipeDetalheView.as_view(), name='equipe-detalhe'),
    path('adm/pessoas/<int:pk>', views.PessoaDetalheView.as_view(), name='pessoa-detalhe'),

    path('adm/instituicoes/add', views.InstituicaoCreateView.as_view(), name='insti-form'),
    path('adm/cursos/add', views.CursoCreateView.as_view(), name='curso-form'),
    path('adm/disciplinas/add', views.DisciplinaCreateView.as_view(), name='disci-form'),
    path('adm/turmas/add', views.TurmaCreateView.as_view(), name='turma-form'),
    path('adm/equipes/add', views.EquipeCreateView.as_view(), name='equipe-form'),
    path('adm/pessoas/add', views.PessoaCreateView.as_view(), name='pessoa-form'),

    path('adm/instituicoes/delete/<int:pk>', views.InstituicaoDeleteView.as_view(), name='delete-insti'),
    path('adm/cursos/delete/<int:pk>', views.CursoDeleteView.as_view(), name='delete-curso'),
    path('adm/disciplinas/delete/<int:pk>', views.DisciplinaDeleteView.as_view(), name='delete-disci'),
    path('adm/turmas/delete/<int:pk>', views.TurmaDeleteView.as_view(), name='delete-turma'),
    path('adm/equipes/delete/<int:pk>', views.EquipeDeleteView.as_view(), name='delete-equipe'),
    path('adm/pessoas/delete/<int:pk>', views.PessoaDeleteView.as_view(), name='delete-pessoas'),

]

urlpatterns += [
    # path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', views.CustomLogoutView.as_view(), name='logout'),
    # path('accounts/change/', views.CustomPasswordChangeView.as_view(), name='change'),
    # path('accounts/reset/', views.CustomPwresetView.as_view(), name='reset'),

    # path('home/adm', views.MyAdmView.as_view(), name='adm'),
]

urlpatterns += urls_api.urlpatterns