from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
# from .views import UserViewSet, GroupViewSet, UsersEquipeView, TurmaUserView, RealNames
from .views import UsersEquipeView, TurmaUserView, RealNames

router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('api/core/', include(router.urls)),
    path('api/core/auth', include('rest_framework.urls', namespace='rest_framework')),
    path('api/core/turmas/user/<int:id>/', TurmaUserView.as_view()),
    path('api/core/turmas/names/<str:tag_turma>/', RealNames.as_view()),
    path('api/core/turmas/names/<str:tag_turma>/<str:tag_equipe>/', RealNames.as_view()),
    path('api/core/equipe/<str:tag_equipe>/users/', UsersEquipeView.as_view())
    ]