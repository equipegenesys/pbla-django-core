from django.forms import ModelForm
from . import models

class InstituicaoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'id': 'form-name', 'class': 'form-control'})

    class Meta:    
        model = models.Instituicao
        fields = ('name',)

class CursoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'id': 'form-name', 'class': 'form-control'})

    class Meta:    
        model = models.Curso
        fields = ('name',)

class DisciplinaForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'id': 'form-name', 'class': 'form-control'})

    class Meta:    
        model = models.Disciplina
        fields = ('name',)

class TurmaForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs.update({'id': 'form-name', 'class': 'form-control'})

    class Meta:    
        model = models.Turma
        fields = ('tag_turma',)

class EquipeForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'id': 'form-name', 'class': 'form-control'})

    class Meta:    
        model = models.Equipe
        fields = ('name',)

class PessoaForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'id': 'form-name', 'class': 'form-control'})

    class Meta:    
        model = models.Pessoa
        fields = ('first_name',)