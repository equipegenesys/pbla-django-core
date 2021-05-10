from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from .views import UserViewSet, GroupViewSet, TurmaViewSet, TurmaUserView, RealNames

# # Serializers define the API representation.
# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'email', 'is_staff']

# # ViewSets define the view behavior.
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
# router.register(r'turmas/user', TurmaUserViewSet)
# router.register(r'turmas/user', TurmaUserView.as_view(), basename='turmas/user')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/core/', include(router.urls)),
    path('api/core/auth', include('rest_framework.urls', namespace='rest_framework')),
    path('api/core/turmas/user/<int:id>/', TurmaUserView.as_view()),
    path('api/core/turmas/names/<str:tag_turma>/', RealNames.as_view()),
    path('api/core/turmas/names/<str:tag_turma>/<str:tag_equipe>/', RealNames.as_view()),
    ]