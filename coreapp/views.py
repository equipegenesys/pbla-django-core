from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import views as contrib_views
from django.urls import reverse
from django.template import loader
from django.views.generic import TemplateView
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


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
