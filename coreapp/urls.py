from django.urls import path
from django.contrib.auth.models import User
from django.contrib.auth import views as contrib_views
from django.conf.urls import include
from pblacore import urls as pblacoreurls

from . import views

urlpatterns = [
    path('home/professor', views.professor, name='professor'),
    path('home/estudante', views.estudante, name='estudante'),
]

# urlpatterns += pblacoreurls
# print(pblacoreurls)
# urlpatterns += [
#     path('accounts/', include('django.contrib.auth.urls')),
# ]

urlpatterns += [
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('redirect/admin/', views.admin_redirect, name='admin')
    # path('accounts/login/', contrib_views.LoginView.as_view(), name='login'),
]