from datetime import datetime

from django import forms
from django.conf import settings
from project.models import vagasEmprego
from tempus_dominus.widgets import DatePicker

from .validator import *


class DateInput(forms.DateInput):
    input_type = 'date'


class JobForm(forms.ModelForm):

    class Meta:
        model = vagasEmprego
        fields = [
            'tituloVaga',
            'area',
            'tipo_vaga',
            'nome_empresa',
            'link_empresa_ou_pesquisa',
            'numeroVagas',
            'horasSemana',
            'valorSalario',
            'dataCadastro',
            'dataFechamento',
            'link_vaga',
            'pdf',
            'professor',
            'aluno',
        ]
        labels = {'numeroVagas': 'Quantidade de vagas <span class="teste">*</span>',
                  'tituloVaga': 'Titulo <span class="teste">*</span>',
                  'area': 'Área <span class="teste">*</span>',
                  'horasSemana': 'Horas semanais <span class="teste">*</span>',
                  'valorSalario': 'Valor da bolsa <span class="teste">*</span>',
                  'dataCadastro': 'Data de cadastro <span class="teste">*</span>',
                  'pdf': 'Informações complementares (PDF) <span class="teste">*</span>',
                  'dataFechamento': 'Data de encerramento da inscrição: <span class="teste">*</span>',
                  'tipo_vaga': 'Tipo <span class="teste">*</span>',
                  'nome_empresa': 'Empresa, Grupo de Pesquisa ou Projeto <span class="teste">*</span>',
                  'link_empresa_ou_pesquisa': 'Link da Empresa, Grupo de Pesquisa ou Projeto',
                  'link_vaga': 'Link para inscrição <span class="teste"></span>'
                  }

        widgets = {
            'dataFechamento': DateInput(attrs={'placeholder': '%d/%m/%Y'}),
            'dataCadastro':  DateInput(),
            'aluno': forms.MultipleHiddenInput,
            'professor': forms.HiddenInput
        }

    def clean(self):
        numero_vagas = self.cleaned_data.get('numeroVagas')
        horas_semana = self.cleaned_data.get('horasSemana')
        valor_salario = self.cleaned_data.get('valorSalario')
        data_cadastro = self.cleaned_data.get('dataCadastro')
        titulo_vaga = self.cleaned_data.get('tituloVaga')
        pdf = self.cleaned_data.get('pdf')
        data_fechamento = self.cleaned_data.get('dataFechamento')
        aluno = self.cleaned_data.get('aluno')
        tipo_vaga = self.cleaned_data.get('tipo_vaga')
        nome_empresa = self.cleaned_data.get('nome_empresa')
        link_vaga = self.cleaned_data.get('link_vaga')

        lista_de_erros = {}

        numero_vagas_invalido(numero_vagas, 'numeroVagas', lista_de_erros)
        horas_semana_invalida(horas_semana, 'horasSemana', lista_de_erros)
        valor_salario_invalido(valor_salario, 'valorSalario', lista_de_erros)
        date_invalid(data_cadastro, data_fechamento,
                     'dataCadastro', lista_de_erros)

        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_error = lista_de_erros[erro]
                self.add_error(erro, mensagem_error)

        return self.cleaned_data

    def is_valid(self):
        result = super().is_valid()
        # loop on *all* fields if key '__all__' found else only on errors:
        for x in (self.fields if '__all__' in self.errors else self.errors):
            attrs = self.fields[x].widget.attrs
            attrs.update({'class': attrs.get('class', '') + ' is-invalid'})

        return result
