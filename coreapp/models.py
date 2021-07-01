from django.conf import settings
from django.db import models
from django.db import transaction
from strgen import StringGenerator as SG
from string import ascii_uppercase as alphabet
from django.contrib.auth.models import User
from django.urls import reverse
from . import gateway

class Pessoa(User):
    # objects = PersonManager()

    class Meta:
        proxy = True
        ordering = ('first_name', )

    def get_fields(self):
        list_of_fields = [(field.name, field.value_to_string(self)) for field in Pessoa._meta.fields]
        partial_list = list()
        
        for i in list_of_fields:
            if i[0] != 'password' and i[0] != 'id':
                partial_list.append(i)

        order = [3, 4, 5, 2, 0, 8, 1, 6, 7]
        partial_list = [partial_list[i] for i in order]
        return partial_list

    def get_absolute_url(self):
        return reverse('pessoa-detalhe', kwargs={'pk': self.pk})

    def __str__(self):
        fullname = self.first_name + " " + self.last_name
        return fullname

class Dash(models.Model):
    pass


class MyEstudante(models.Model):
    pass


class MyAdm(models.Model):
    pass


class Instituicao(models.Model):
    name = models.CharField(max_length=300)
    # pub_date = models.DateTimeField('date published')

    def get_absolute_url(self):
        return reverse('insti-detalhe', kwargs={'pk': self.pk})

    def get_fields(self):
        list_of_fields = [(field.name, field.value_to_string(self)) for field in Instituicao._meta.fields]
        return list_of_fields

    def __str__(self):
        return self.name


class Curso(models.Model):
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    nivel = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse('curso-detalhe', kwargs={'pk': self.pk})

    def get_fields(self):
        list_of_fields = [(field.name, field.value_to_string(self)) for field in Curso._meta.fields]
        return list_of_fields

    def __str__(self):
        return f'{self.nivel} - {self.name}'


class Disciplina(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    tag_disciplina = models.CharField(max_length=20, unique=True, null=True,
                                      default=None, help_text="A tag da disciplina é gerada automaticamente.")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        iniciais = str()
        words = self.name.split(' ')
        with open('coreapp/stopwords.txt', 'r') as stopwords:
            stopwords = stopwords.read().splitlines()
            name_words = [i for i in words if i not in stopwords]
        for word in name_words:
            iniciais = iniciais + word[:1]
        if len(iniciais) > 3:
            iniciais = iniciais[:3]
        elif len(iniciais) < 3:
            if len(iniciais) == 2:
                iniciais = iniciais + str(0)
            if len(iniciais) == 1:
                iniciais = iniciais + str(00)
        iniciais = iniciais.upper()
        nova_tag_disciplina = SG(iniciais+'[A-Z0-9]{3}').render()
        trials = 1
        success = False
        while not success:
            try:
                with transaction.atomic():
                    if self.tag_disciplina == None:
                        self.tag_disciplina = nova_tag_disciplina
                        super().save(update_fields=['tag_disciplina'])
                    elif self.tag_disciplina == nova_tag_disciplina:
                        pass
            except:
                trials = trials + 1
                if trials > 20:
                    raise
                else:
                    self.tag_disciplina = SG(iniciais+'[A-Z0-9]{3}').render()
            else:
                success = True

    def get_absolute_url(self):
        return reverse('disci-detalhe', kwargs={'pk': self.pk})

    def get_fields(self):
        list_of_fields = [(field.name, field.value_to_string(self)) for field in Disciplina._meta.fields]
        return list_of_fields

    def __str__(self):
        return self.name + " - " + self.tag_disciplina


class Turma(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    ano = models.IntegerField()
    semestre = models.IntegerField()
    tag_turma = models.CharField(max_length=20, unique=True, null=True,
                                 default=None, help_text="A tag da turma é gerada automaticamente.")
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.tag_turma = self.disciplina.tag_disciplina + \
            str(self.ano) + str(self.semestre)
        trials = 1
        success = False
        while not success:
            try:
                with transaction.atomic():
                    # pass
                    super().save(update_fields=['tag_turma'])
            except:
                if trials > 20:
                    raise
                else:
                    self.tag_turma = self.disciplina.tag_disciplina + \
                        str(self.ano) + str(self.semestre) + \
                        str(alphabet[trials])
                    trials = trials + 1
            else:
                success = True

    def get_absolute_url(self):
        return reverse('turma-detalhe', kwargs={'pk': self.pk})

    def get_fields(self):
        list_of_fields = [(field.name, field.value_to_string(self)) for field in Turma._meta.fields]
        return list_of_fields

    def __str__(self):
        return f'{self.disciplina.name} - {self.ano}.{self.semestre} - {self.tag_turma}'


class Equipe(models.Model):
    name = models.CharField(max_length=200)
    turma = models.ManyToManyField(Turma)
    tag_equipe = models.CharField(max_length=20, unique=True, null=True,
                                  default=None, help_text="A tag da equipe é gerada automaticamente.")
    user = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        nova_tag_equipe = SG('[A-Z0-9]{4}').render()
        trials = 1
        success = False
        while not success:
            try:
                with transaction.atomic():
                    if self.tag_equipe == None:
                        self.tag_equipe = nova_tag_equipe
                        super().save(update_fields=['tag_equipe'])
                    elif self.tag_equipe == nova_tag_equipe:
                        pass
            except:
                trials = trials + 1
                if trials > 2000:
                    raise
                else:
                    self.tag_equipe = SG('[A-Z0-9]{4}').render()
            else:
                success = True

    def get_absolute_url(self):
        return reverse('equipe-detalhe', kwargs={'pk': self.pk})

    def get_fields(self):
        list_of_fields = [(field.name, field.value_to_string(self)) for field in Equipe._meta.fields]
        return list_of_fields

    def __str__(self):
        return f'{self.name} - {self.tag_equipe}'


class Integracao(models.Model):
    name = models.CharField(max_length=50, blank=False)
    root_endpoint = models.CharField(max_length=100)
    pessoa = models.ManyToManyField(Pessoa, through='UserIntegBridge')
    equipe = models.ManyToManyField(Equipe, through='EquipeIntegBridge')
    instituicao = models.ManyToManyField(Instituicao, through='InstituicaoIntegBridge')

    def __str__(self):
        return self.name

class UserIntegBridge(models.Model):
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    integracao = models.ForeignKey(Integracao, on_delete=models.CASCADE)
    first_created = models.DateTimeField(auto_now_add=True)
    is_active_update_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField()
    def integ_status(self):
        if gateway.get_integ_status(integ = self.integracao.name, user_id = self.pessoa.pk) == 'true':
            return 'Conectado'
        else: 
            return 'Não conectado'
    def get_pessoa_id(self):
        return self.pessoa.pk
    def get_integ_id(self):
        return self.integracao.pk

class EquipeIntegBridge(models.Model):
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE)
    integracao = models.ForeignKey(Integracao, on_delete=models.CASCADE)    
    first_created = models.DateTimeField(auto_now_add=True)
    is_active_update_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField()

class InstituicaoIntegBridge(models.Model):
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE)
    integracao = models.ForeignKey(Integracao, on_delete=models.CASCADE)    
    first_created = models.DateTimeField(auto_now_add=True)
    is_active_update_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField()
    def integ_status(self):
        # print('HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH',self.integracao.name)
        if gateway.get_integ_status(integ = self.integracao.name) == 'true':
            return 'Conectado'
        else: 
            return 'Não conectado'
    def get_insti_id(self):
        return self.instituicao.pk
    def get_integ_id(self):
        return self.integracao.pk
    


class TurmasClass(object):
    user_id = None    
    
    def get_turmas(self, user_id: int):
        turmas_from_user = Turma.user.through.objects.filter(
            user_id=user_id)
        turma_equipe_dict = dict()
        result_dict = {'user': user_id,
                       'turma-equipe': turma_equipe_dict}

        for turma in turmas_from_user:
            equipes_from_user = Equipe.objects.filter(
                user__id=user_id).filter(turma__id=turma.turma_id)
            turma = Turma.objects.get(pk=turma.turma_id)

            if equipes_from_user:
                for equipe in equipes_from_user:
                    turma_equipe_dict[turma.tag_turma] = equipe.tag_equipe
            else:
                turma_equipe_dict[turma.tag_turma] = None

        return result_dict

    # def __init__(self, *args, **kw):
    #     user_id = None

class TurmaEquipe(object):
    tag_turma = None

    def get_name(self, tag_equipe: str, **kwargs):
        tag_turma = kwargs.get('tag_turma')
        turma_equipe_dict = dict()       
        equipe = Equipe.objects.get(tag_equipe=tag_equipe)
        turma_equipe_dict['Equipe'] = equipe.name
        
        if tag_turma != 'all':  
            turma = Turma.objects.get(tag_turma=tag_turma)
            turma_equipe_dict['Disciplina'] = turma.disciplina.name
            turma_equipe_dict['Semestre'] = str(
                turma.ano) + "." + str(turma.semestre)
        else:
            turma_equipe_dict['Disciplina'] = 'Todas as disicplinas'
            turma_equipe_dict['Semestre'] = 'Todos os semestres'

        # print(turma_equipe_dict)

        return turma_equipe_dict


