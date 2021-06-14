from django import forms
from . import models
from django.contrib.auth.hashers import make_password


class InstituicaoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'id': 'form-name', 'class': 'form-control'})

    class Meta:    
        model = models.Instituicao
        fields = ('name',)

class CursoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['instituicao'].widget.attrs.update({'id': 'form-name', 'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'id': 'form-name', 'class': 'form-control'})
        self.fields['nivel'].widget.attrs.update({'id': 'form-name', 'class': 'form-control'})

    class Meta:    
        model = models.Curso
        fields = ('instituicao', 'name', 'nivel',)

class DisciplinaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['curso'].widget.attrs.update({'id': 'form-name', 'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'id': 'form-name', 'class': 'form-control'})

    class Meta:    
        model = models.Disciplina
        fields = ('curso', 'name',)

class TurmaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['disciplina'].widget.attrs.update({'id': 'form-name', 'class': 'form-control'})
        self.fields['ano'].widget.attrs.update({'id': 'form-name', 'class': 'form-control'})
        self.fields['semestre'].widget.attrs.update({'id': 'form-name', 'class': 'form-control'})
        self.fields['user'].widget.attrs.update({'id': 'form-name', 'class': 'form-control'})

    class Meta:    
        model = models.Turma
        fields = ('disciplina', 'ano', 'semestre', 'user', )

class EquipeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'id': 'form-name', 'class': 'form-control'})
        self.fields['turma'].widget.attrs.update({'id': 'form-name', 'class': 'form-control'})
        self.fields['user'].widget.attrs.update({'id': 'form-name', 'class': 'form-control'})

    class Meta:    
        model = models.Equipe
        fields = ('name', 'turma', 'user',)

class PessoaForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        # self.fields['is_superuser'].widget.attrs.update({'id': 'form-name', 'class': 'form-control'})
        # self.fields['is_staff'].widget.attrs.update({'id': 'form-check', 'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        self.fields['groups'].widget.attrs.update({'class': 'form-control'})

    class Meta:    
        model = models.Pessoa
        fields = ('first_name', 'last_name', 'email', 'username', 'password', 'groups', )

    def save(self, commit=True):
        pessoa = super(PessoaForm, self).save(commit=False)
        pessoa.set_password(self.cleaned_data["password"])
        if commit:
            pessoa.save()
        return pessoa

# <input type="checkbox" name="is_staff" id="form-name" class="form-control">