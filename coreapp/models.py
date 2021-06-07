from django.conf import settings
from django.db import models
# from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.db import transaction
from strgen import StringGenerator as SG
from string import ascii_uppercase as alphabet
from django.contrib.auth.models import User, Group, AbstractUser

# from django.contrib.auth.models import AbstractUser

# class ExtendedUser(AbstractUser):
#     pass
    # first_name = models.Field(verbose_name = "Nome")

class Dash(models.Model):
    pass


class MyEstudante(models.Model):
    pass


class MyAdm(models.Model):
    pass


class Instituicao(models.Model):
    name = models.CharField(max_length=300)
    # pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.name


class Curso(models.Model):
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    nivel = models.CharField(max_length=200)

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

    def __str__(self):
        return f'{self.name} - {self.tag_equipe}'


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

    def get_name(self, tag_turma: str, **kwargs):
        turma_equipe_dict = dict()        
        turma = Turma.objects.get(tag_turma=tag_turma)
        tag_equipe = kwargs.get('tag_equipe')

        turma_equipe_dict['Disciplina'] = turma.disciplina.name
        turma_equipe_dict['Semestre'] = str(
            turma.ano) + "." + str(turma.semestre)
        
        if tag_equipe:
            equipe = Equipe.objects.get(tag_equipe=tag_equipe)
            turma_equipe_dict['Equipe'] = equipe.name

        # print(turma_equipe_dict)

        return turma_equipe_dict

