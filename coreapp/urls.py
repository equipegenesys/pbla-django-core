from django.urls import path
from django.contrib.auth.models import User
from django.contrib.auth import views as contrib_views
from django.conf.urls import include
from pblacore import urls as pblacoreurls
from . import views, urls_api

urlpatterns = [
    path('home/professor', views.Professor.as_view(), name='professor'),
    # path('home/professor', views.professor, name='professor'),
    path('home/estudante', views.Estudante.as_view(), name='estudante'),
    



    
    # path('django_plotly_dash/', include('django_plotly_dash.urls')),
]

# urlpatterns += pblacoreurls
# print(pblacoreurls)
# urlpatterns += [
#     path('accounts/', include('django.contrib.auth.urls')),
# ]

urlpatterns += [
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    # path('redirect/admin/', views.admin_redirect, name='admin'),
    path('home/adm', views.MyAdmView.as_view(), name='adm'),
    # path('accounts/login/', contrib_views.LoginView.as_view(), name='login'),
    path('home/estudante/turmas/', views.TurmasFromUser.as_view(), name='turmas'),

]

urlpatterns += urls_api.urlpatterns