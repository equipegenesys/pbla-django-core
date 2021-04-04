from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import views as contrib_views
from django.urls import reverse

class CustomLoginView(contrib_views.LoginView):

    def get_success_url(self):
        group_list = self.request.user.groups.values_list('name',flat = True)
        group_list = list(group_list)
        if 'professores' in group_list:
            return reverse("professor")
        elif 'estudantes' in group_list:
            return reverse("estudante")
        else:
            if self.request.user.is_staff:
                print("é admin")
                return reverse("admin")

def professor(request):
    return HttpResponse("Você está na home do professor.")

def estudante(request):
    return HttpResponse("Você está na home do estudante.")

def admin_redirect(request):
    return HttpResponse('Você é administrador. Acesse <a href="https://analytics.pbl.tec.br/admin/">aqui</a> o portal de administração.')