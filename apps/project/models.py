from datetime import date

from accounts.models import User, UserProfile
from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField


# Create your models here.
class Professor(models.Model):
    nomeProfessor = models.CharField(max_length=255)
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Professor(a)'
        verbose_name_plural = 'Professores(as)'

    def __str__(self):
        return self.nomeProfessor


class vagasEmprego(models.Model):
    disponivel = (
        ('S', 'Sim'),
        ('N', 'Não')
    )

    tipo_vaga = {
        ('PIC', 'Projeto de iniciação científica'),
        ('PIT', 'Projeto de iniciação tecnológica'),
        ('PE', 'Projeto de extensão'),
        ('ES', 'Estágio'),
        ('PD', 'Projeto de desenvolvimento')
    }

    areas = {
        ('Adm', 'Administração'),
        ('Atp', 'Antropologia'),
        ('CC', 'Ciências Contábeis'),
        ('Com', 'Computação'),
        ('Dsg', 'Design'),
        ('Eco', 'Ecologia'),
        ('Mat', 'Matemática'),
        ('Ped', 'Pedagogia'),
        ('Sec', 'Secretariado')
    }

    numeroVagas = models.IntegerField("Número de vagas")
    horasSemana = models.IntegerField("Horas Semana")
    valorSalario = models.FloatField("Valor Salario")
    dataCadastro = models.DateField("Data de cadastro", default=timezone.now)
    tituloVaga = models.CharField("Titulo da Vaga", max_length=255)
    pdf = models.CharField("Link do pdf", max_length=255)
    dataFechamento = models.DateField("Data de Fechamento")
    professor = models.ForeignKey(Professor, on_delete=models.PROTECT)
    aluno = models.ManyToManyField(
        UserProfile, blank=True)
    disponivel = models.CharField(max_length=1, default="S")
    tipo_vaga = models.CharField(max_length=3, choices=tipo_vaga)
    nome_empresa = models.CharField(
        "Nome empresa ou nome projeto", max_length=17)
    link_empresa_ou_pesquisa = models.CharField(
        "Link empresa ou grupo de projeto", max_length=255, blank=True, null=True)
    link_vaga = models.CharField(
        "Link da vaga", max_length=255, blank=True, null=True)
    area = models.CharField(max_length=3, choices=areas, default="Com")

    @property
    def is_closed(self):
        return date.today() > self.dataFechamento

    def __str__(self):
        return self.tituloVaga

    def get_area_display(self):
        return dict(self.areas).get(self.area, self.area)
