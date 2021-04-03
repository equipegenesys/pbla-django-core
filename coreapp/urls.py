from django.urls import path
from django.contrib.auth.models import User
from django.conf.urls import include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

# urlpatterns += [
#     path('accounts/login/', views.CustomLoginView, name='login'),
# ]