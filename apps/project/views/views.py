import datetime
import os

from accounts.models import User, UserProfile
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from project.forms import JobForm
from project.models import Professor, vagasEmprego


# View of vagas
def index(request):
    dados = {}

    vagas = vagasEmprego.objects.all().filter(
        disponivel='S').order_by('-dataFechamento')

    if request.user.is_authenticated:
        user = request.user
        user_info = None

        aluno = get_object_or_404(UserProfile, user=user)

        if user.user_is_teacher:
            user_info = Professor.objects.filter(user=request.user.id).first()
        else:
            user_info = get_object_or_404(UserProfile, user=user)

        dados['user'] = user
        dados['user_info'] = user_info

    paginator = Paginator(vagas, 6)
    page = request.GET.get('page')
    vagas_per_page = paginator.get_page(page)
    dados['vagas'] = vagas_per_page
    dados['title'] = "Home"

    return render(request, 'project/index.html', dados)


def view_vaga(request, vaga_id):
    vaga = get_object_or_404(
        vagasEmprego.objects.select_related('professor'), id=vaga_id)

    dados = {}

    dados['vaga'] = vaga
    dados['title'] = 'Visualizar vaga'

    return render(request, 'project/view_vaga.html', dados)


@login_required
def create_vaga(request):
    if not request.user.user_is_teacher:
        messages.error(request, "Você não pode realizar essa operação!")
        return redirect("index")

    context = {}
    date = datetime.datetime.today().strftime('%Y-%m-%d')

    user = Professor.objects.filter(user=request.user.id).first()

    # print(user)
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES or None, initial={
            "professor": user, "dataCadastro": date})

        if form.is_valid():
            # print('passou')
            form.save()
            return redirect('minhas_vagas')

    else:
        form = JobForm(initial={
            "professor": user, "dataCadastro": date})

    context['form'] = form
    context['professor'] = user
    context['title'] = "Cadastrar vagas"

    return render(request, 'project/forms.html', context)


@login_required
def change_vaga(request, vaga_id):
    if not request.user.user_is_teacher:
        messages.error(request, "Você não pode realizar essa operação!")
        return redirect("index")

    nome = request.user

    context = {}
    job = get_object_or_404(vagasEmprego, pk=vaga_id)
    job.dataCadastro = job.dataCadastro.strftime('%Y-%m-%d')
    job.dataFechamento = job.dataFechamento.strftime('%Y-%m-%d')

    if job.professor.user != nome:
        messages.error(request, "Você não pode realizar essa operação!")
        return redirect("index")

    if request.method != "POST":
        form = JobForm(instance=job)
    elif request.method == "POST":
        form = JobForm(request.POST,
                       files=request.FILES, instance=job)

        if form.is_valid():

            # print(form.id)

            form.save()
            messages.success(request, "Vaga de emprego alterado com sucesso!")
            return redirect('minhas_vagas')

    context["form"] = form
    context["title"] = "Alterar vaga"

    return render(request, "project/forms.html", context)


def search(request):
    dados = {}

    vagas = vagasEmprego.objects.all().filter(
        disponivel='S').order_by('-dataFechamento')

    if request.user.is_authenticated:
        user = request.user
        user_info = None

        if user.user_is_teacher:
            user_info = Professor.objects.filter(user=request.user.id).first()
        else:
            user_info = get_object_or_404(UserProfile, user=user)

        dados['user'] = user
        dados['user_info'] = user_info

    if 'search' in request.GET:
        search_name = request.GET['search']
        if search_name:
            vagas = vagas.filter(tituloVaga__icontains=search_name)

    dados = {
        'vagas': vagas,
        'title': 'Filtrar vagas',
    }

    return render(request, 'project/search.html', dados)


@login_required
def delete_job(request, vaga_id):
    if not request.user.user_is_teacher:
        messages.error(request, "Você não pode realizar essa operação!")
        return redirect("index")

    nome = request.user

    context = {}
    job = get_object_or_404(vagasEmprego, pk=vaga_id)
    context['title'] = 'Deletar vaga'
    context['vaga'] = job

    if job.professor.user != nome:
        messages.error(request, "Você não pode realizar essa operação!")
        return redirect("index")

    if request.method == "POST":
        job.delete()

        messages.success(request, "Vaga deletada com sucesso")

        return redirect('minhas_vagas')

    return render(request, 'project/delete.html', context)


@login_required
def minhas_vagas(request):
    if not request.user.user_is_teacher:
        messages.error(request, "Você não pode realizar essa operação!")
        return redirect("index")

    professor = Professor.objects.filter(user=request.user.id).first()

    vagas = vagasEmprego.objects.all().filter(
        professor=professor).order_by('-dataFechamento')

    paginator = Paginator(vagas, 6)
    page = request.GET.get('page')
    vagas_per_page = paginator.get_page(page)

    dados = {}

    dados['vagas'] = vagas_per_page
    dados['title'] = "Minhas oportunidades"

    return render(request, 'project/dashboard.html', dados)


@login_required
def inscrever_aluno(request, vaga_id):
    data_hoje = datetime.datetime.today().date()

    if request.user.user_is_teacher:
        messages.error(
            request, "Você não pode realizar essa operação! Por ser professor")
        return redirect("index")

    user = request.user.id

    aluno = get_object_or_404(UserProfile, user=user)

    if aluno == None:
        messages.error(request, "Erro você não é aluno")
        return redirect("index")

    job = get_object_or_404(vagasEmprego, pk=vaga_id)

    if aluno in job.aluno.all():
        messages.error(request, "Você já demonstrou interesse nessa vaga")
        return redirect("index")

    if job == None:
        messages.error(request, "Vaga não existe!")
        return redirect("index")

    if data_hoje > job.dataFechamento:
        messages.error(request, "Vaga não está aberta!")
        return redirect("index")

    if aluno.is_verify == False:
        messages.error(request, "Você não completou suas informações!")
        return redirect("profile")

    job.aluno.add(aluno)

    return redirect('index')


@login_required
def desinscrever_aluno(request, vaga_id):
    if request.user.user_is_teacher:
        messages.error(
            request, "Você não pode realizar essa operação! Por ser professor")
        return redirect("index")

    user = request.user.id

    aluno = get_object_or_404(UserProfile, user=user)

    if aluno == None:
        messages.error(request, "Erro você não é aluno")
        return redirect("index")

    job = get_object_or_404(vagasEmprego, pk=vaga_id)

    data_hoje = datetime.datetime.today().date()

    if data_hoje > job.dataFechamento:
        messages.error(request, "Vaga não está aberta!")
        return redirect("index")

    if aluno in job.aluno.all():
        job = get_object_or_404(vagasEmprego, pk=vaga_id)

        if job == None:
            messages.error(request, "Vaga não existe!")
            return redirect("index")

        job.aluno.remove(aluno)

        job.save()

        return redirect("index")

    messages.error(request, "Você não possui interesse nessa vaga!")
    return redirect('index')


def projeto_cientifico(request):
    dados = {}

    vagas = vagasEmprego.objects.all().filter(
        disponivel='S').filter(tipo_vaga='PIC').order_by('-dataFechamento')

    if request.user.is_authenticated:
        user = request.user
        user_info = None

        aluno = get_object_or_404(UserProfile, user=user)

        if user.user_is_teacher:
            user_info = Professor.objects.filter(user=request.user.id).first()
        else:
            user_info = get_object_or_404(UserProfile, user=user)

        dados['user'] = user
        dados['user_info'] = user_info

    paginator = Paginator(vagas, 6)
    page = request.GET.get('page')
    vagas_per_page = paginator.get_page(page)

    dados['vagas'] = vagas_per_page
    dados['title'] = "Projetos de iniciação científica"

    return render(request, 'project/cientifico.html', dados)


def projeto_tecnologico(request):
    dados = {}

    vagas = vagasEmprego.objects.all().filter(
        disponivel='S').filter(tipo_vaga='PIT').order_by('-dataFechamento')

    if request.user.is_authenticated:
        user = request.user
        user_info = None

        aluno = get_object_or_404(UserProfile, user=user)

        if user.user_is_teacher:
            user_info = Professor.objects.filter(user=request.user.id).first()
        else:
            user_info = get_object_or_404(UserProfile, user=user)

        dados['user'] = user
        dados['user_info'] = user_info

    paginator = Paginator(vagas, 6)
    page = request.GET.get('page')
    vagas_per_page = paginator.get_page(page)

    dados['vagas'] = vagas_per_page
    dados['title'] = "Projetos de iniciação tecnológica"

    return render(request, 'project/tecnologico.html', dados)


def projeto_extencao(request):
    dados = {}

    vagas = vagasEmprego.objects.filter(
        disponivel='S').filter(tipo_vaga='PE').order_by('-dataFechamento')

    if request.user.is_authenticated:
        user = request.user
        user_info = None

        aluno = get_object_or_404(UserProfile, user=user)

        if user.user_is_teacher:
            user_info = Professor.objects.filter(user=request.user.id).first()
        else:
            user_info = get_object_or_404(UserProfile, user=user)

        dados['user'] = user
        dados['user_info'] = user_info

    paginator = Paginator(vagas, 6)
    page = request.GET.get('page')
    vagas_per_page = paginator.get_page(page)

    dados['vagas'] = vagas_per_page
    dados['title'] = "Projetos de extensão"

    return render(request, 'project/extensao.html', dados)


def estagio(request):
    dados = {}

    vagas = vagasEmprego.objects.filter(
        disponivel='S').filter(tipo_vaga='ES').order_by('-dataFechamento')

    if request.user.is_authenticated:
        user = request.user
        user_info = None

        aluno = get_object_or_404(UserProfile, user=user)

        if user.user_is_teacher:
            user_info = Professor.objects.filter(user=request.user.id).first()
        else:
            user_info = get_object_or_404(UserProfile, user=user)

        dados['user'] = user
        dados['user_info'] = user_info

    paginator = Paginator(vagas, 6)
    page = request.GET.get('page')
    vagas_per_page = paginator.get_page(page)

    dados['vagas'] = vagas_per_page
    dados['title'] = "Estágios"

    return render(request, 'project/estagio.html', dados)


def projeto_desenvolvimento(request):
    dados = {}

    vagas = vagasEmprego.objects.filter(
        disponivel='S').filter(tipo_vaga='PD').order_by('-dataFechamento')

    if request.user.is_authenticated:
        user = request.user
        user_info = None

        aluno = get_object_or_404(UserProfile, user=user)

        if user.user_is_teacher:
            user_info = Professor.objects.filter(user=request.user.id).first()
        else:
            user_info = get_object_or_404(UserProfile, user=user)

        dados['user'] = user
        dados['user_info'] = user_info

    paginator = Paginator(vagas, 6)
    page = request.GET.get('page')
    vagas_per_page = paginator.get_page(page)

    dados['vagas'] = vagas_per_page
    dados['title'] = "Projetos de desenvolvimento"

    return render(request, 'project/projetos_desenvolvimento.html', dados)


def filter_area(request, area):
    tipo_area_dict = {
        code: display for code, display in vagasEmprego.areas
    }

    dados = {}

    if area not in tipo_area_dict:
        raise Http404("Área inválida")

    display_name = tipo_area_dict[area]

    vagas = vagasEmprego.objects.filter(
        disponivel='S').filter(area=area).order_by('-dataFechamento')

    if request.user.is_authenticated:
        user = request.user
        user_info = None

        aluno = get_object_or_404(UserProfile, user=user)

        if user.user_is_teacher:
            user_info = Professor.objects.filter(user=request.user.id).first()
        else:
            user_info = get_object_or_404(UserProfile, user=user)

        dados['user'] = user
        dados['user_info'] = user_info

    paginator = Paginator(vagas, 6)
    page = request.GET.get('page')
    vagas_per_page = paginator.get_page(page)

    dados['vagas'] = vagas_per_page
    dados['title'] = "Vagas de " + display_name
    dados['tipo_vaga'] = display_name

    return render(request, 'project/filter_area.html', dados)
