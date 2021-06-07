# tutorial/tables.py
import django_tables2 as tables
from django.contrib.auth.models import User, Group
# from .models import ExtendedUser

class PersonTable(tables.Table):
    class Meta:
        model = User
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", "first_name", "last_name", "email", "is_staff", )