import csv
import datetime
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags

from gestao_eventos.utils import enviar_email
from tipos.forms import EventoForm, ParticipanteForm, InscricaoForm
from tipos.models import Evento, Participante, Inscricao, ImagemEvento
from tipos.services.geocode import get_coordinates_from_address
from tipos.services.search_address_by_cep import buscar_endereco_por_cep
from tipos.urls import Conferencia, Palestra, Workshop


# Página inicial
def index(request):
    return render(request, 'index.html')


# Adicionar Participante
@login_required
def adicionar_participante(request):
    if request.method == 'POST':
        form = ParticipanteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_participantes')
    else:
        form = ParticipanteForm()
    return render(request, 'paticipantes/form_participante.html', {'form': form, 'title': 'Adicionar Participante'})


# Editar Participante
@login_required
def editar_participante(request, participante_id):
    participante = get_object_or_404(Participante, id=participante_id)
    if request.method == 'POST':
        form = ParticipanteForm(request.POST)
        form.save()

        return redirect('list_participantes')
    else:
        form = ParticipanteForm(instance=participante)
    return render(request, 'participantes/form_participante.html', {'form': form, 'title': 'Editar Participante'})


# Listagem de Participantes
@login_required
def list_participantes(request, participantes=None):
    inquilinos = Participante.objects.all()
    return render(request, 'participantes/list_participantes.html', {'participantes': participantes})


# Excluir Participante
@login_required
def excluir_participante(request, participante_id):
    participante = get_object_or_404(Participante, id=participante_id)
    if request.method == 'POST':
        participante.delete()
        return redirect('list_inquilinos')
    return render(request, 'participantes/excluir_participante.html', {'participante': participante})


# Buscar CEP
@login_required
def buscar_endereco(request):
    cep = request.GET.get('cep')
    if not cep:
        return JsonResponse({'erro': 'CEP não fornecido.'}, status=400)

    try:
        dados = buscar_endereco_por_cep(cep)
        return JsonResponse({
            'endereco': dados['logradouro'],
            'bairro': dados['bairro'],
            'cidade': dados['localidade'],
            'estado': dados['uf'],
            'cep': dados['cep'],
        })
    except Exception as e:
        return JsonResponse({'erro': f'Erro: {str(e)}'}, status=500)


def detalhar_evento(request, imovel_id):
    evento = get_object_or_404(Evento, id=evento_id)
    imagens = evento.imagens.all()

    print(imagens)

    latitude, longitude, display_name = get_coordinates_from_address(cep=evento.cep)

    return render(request, 'eventos/detalhar_evento.html', {
        'evento': evento,
        'imagens': imagens,
        'latitude': latitude,
        'longitude': longitude,
        'display_name': display_name
    })


# Vitrine de Eventos
def vitrine_eventos(request):
    # Filtra os evento que não possuem participantes (eventos disponíveis)
    eventos_disponiveis = Evento.objects.filter(~Q(id__in=Inscricao.objects.values('participante__evento_id')))

    # Para cada imóvel disponível, tenta pegar a imagem destacada ou a primeira imagem disponível
    for eventos in eventos_disponiveis:
        # Busca a imagem destacada ou, caso não tenha, pega a primeira imagem
        imagem_destaque = eventos.imagens.filter(destaque=True).first() or eventos.imagens.first()
        eventos.imagem_destaque = imagem_destaque  # Adiciona dinamicamente o atributo para facilitar o uso no template

    return render(request, 'eventos/vitrine.html', {'eventos': eventos_disponiveis})


# Listagem de Eventos
def listar_eventos(request):
    query = Evento.objects.all()
    data_inicio = request.GET.get('data_inicio')
    hora_inicio = request.GET.get('hota_inicio')
    endereco = request.GET.get('endereco')
    cidade = request.GET.get('cidade')
    estado = request.GET.get('estado')
    valor_min = request.GET.get('valor_min')
    valor_max = request.GET.get('valor_max')

    if cidade:
        query = query.filter(cidade__icontains=cidade)
    if estado:
        query = query.filter(estado__icontains=estado)

    if valor_min and valor_max:
        query = query.filter(valor_inscricao__gte=valor_min, valor_inscricao__lte=valor_max)
    elif valor_min:
        query = query.filter(valor_inscricao__lte=valor_min)  # Less Than or Equal (Menor ou igual)
    elif valor_max:
        query = query.filter(valor_inscricao__gte=valor_max)  # Greater Than or Equal (Maior ou igual)

    return render(request, 'eventos/listar_eventos.html', {'eventos': query})


# Adicionar Evento
@login_required
def adicionar_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            evento = form.save()

            print(f'============> {request.FILES}')
            for imagem in request.FILES.getlist('imagens'):
                print(f'============> {imagem}')
                ImagemEvento.objects.create(evento=evento, imagem=imagem)

            return redirect('lista_eventos')
    else:
        form = EventoForm()
    return render(request, 'eventos/form_evento.html', {'form': form, 'title': 'Adicionar Evento'})


# Editar Evento
@login_required
def editar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES, instance=evento)
        evento = form.save()

        print(f'============> {request.FILES}')
        for imagem in request.FILES.getlist('imagens'):
            print(f'============> {imagem}')
            ImagemEvento.objects.create(evento=evento, imagem=imagem)

        return redirect('listar_eventos')
    else:
        form = EventoForm(instance=evento)
    return render(request, 'eventos/form_evento.html', {'form': form, 'title': 'Editar Evento'})


# Excluir Evento
@login_required
def excluir_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    if request.method == 'POST':
        evento.delete()
        return redirect('listar_eventos')
    return render(request, 'eventos/excluir_eventos.html', {'evento': evento})


@login_required
def preco_evento(request, evento_id):
    try:
        evento = get_object_or_404(Evento, id=evento_id)
        return JsonResponse({'valor_inscricao': str(evento.valor_inscricao)})
    except Evento.DoesNotExist:
        return JsonResponse({'error': 'Evento não encontrado'}, status=404)


# Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'login.html', {'error': 'Credenciais inválidas.'})
    return render(request, 'login.html')


# Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def relatorio_pagamentos(request):
    inscricoes = Inscricao.objects.all()
    total_recebido = inscricoes.filter(pago=True).aggregate(Sum('valor'))['valor__sum'] or 0
    inscricoes_pendentes = inscricoes.filter(pago=False)

    # Notificações de vencimento próximos
    hoje = datetime.date.today()
    vencimento_proximo = hoje + datetime.timedelta(days=7)
    data_pagamento = inscricoes.filter(pago=False, data_pagamento__gt=hoje, data_pagamento__lte=vencimento_proximo)
    inscricoes_nao_pagas = inscricoes.filter(pago=False, data_pagamento__lt=hoje)

    if data_pagamento.exists():
        messages.info(request, f"{data_pagamento.count()} pagamento(s) esta(ão) próximo(s) do vencimento.")

    if inscricoes_nao_pagas.exists():
        messages.error(request, f"{inscricoes_nao_pagas.count()} pagamento(s) que esta(ão) vencimento(s).")

    return render(request, 'relatorios/relatorio_pagamentos.html', {
        'inscricoes': inscricoes,
        'total_recebido': total_recebido,
        'data_pagamento': data_pagamento,
        'inscricoes_nao_pagas': inscricoes_nao_pagas
    })


@login_required
def exportar_relatorio_csv(request):
    # Cria a responsa do tipo CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="relatorio_pagamentos.csv"'
    response.write('\ufeff')  # BOM(Byte Order Mark) do UTF-8

    # Escreve o cabeçalho e os dados no CSV
    writer = csv.writer(response)
    writer.writerow(['Evento', 'Participante', 'Data do Pagamento', 'Valor', 'Pago'])

    # Obtém os dados da Inscrição
    inscricoes = Inscricao.objects.all()

    for inscricao in inscricoes:
        writer.writerow([
            inscricao.evento.endereco,
            inscricao.participante.nome,
            inscricao.data_vencimento,
            f"{inscricao.valor:.0f}",
            'Sim' if inscricao.pago else 'Não'
        ])

    return response


@login_required
def relatorio_avancado_json(request):
    """
    View para fornecer dados em JSON para relatórios avançados com gráficos.
    """
    inscricoes = Inscricao.objects.filter(pago=True).values('data_pagamento').annotate(total=Sum('valor'))
    return JsonResponse(list(inscricoes), safe=False)


@login_required
def listar_inscricoes(request):
    inscricoes = Inscricao.objects.all()
    return render(request, 'inscricoes/listar_inscricoes.html', {'inscricoes': inscricoes})


@login_required
def adicionar_inscricao(request):
    if request.method == 'POST':
        form = InscricaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_inscricoes')
    else:
        form = InscricaoForm()
    return render(request, 'inscriçoes/form_inscricao.html', {'form': form, 'title': 'Cadastrar Inscricao'})


@login_required
def editar_inscricao(request, aluguel_id):
    inscricao = get_object_or_404(Inscricao, id=inscricao_id)

    if request.method == 'POST':
        form = InscricaoForm(request.POST, instance=inscricao)
        if form.is_valid():
            form.save()
            return redirect('listar_inscricoes')
    else:
        form = InscricaoForm(instance=inscricao)

    # Obtenha o preço do valor da inscrição no evento, se houver
    if inscricao.evento:
        valor_inscricao = inscricao.evento.valor_inscricao
    else:
        valor_inscricao = Decimal(0.0)

    return render(request, 'inscricoes/form_inscricao.html', {
        'form': form,
        'inscricao': inscricao,
        'valor_inscricao': valor_inscricao,
        'title': 'Editar Inscricao'
    })


@login_required
def excluir_inscricao(request, inscricao_id):
    inscricao = get_object_or_404(Inscricao, id=inscricao_id)

    if request.method == 'POST':
        inscricao.delete()
        return redirect('listar_incricoes')

    return render(request, 'inscricoes/excluir_inscricao.html', {'inscricao': inscricao})


@login_required
def marcar_como_pago(request, inscricao_id):
    inscricao = get_object_or_404(Inscricao, id=inscricao_id)

    if not inscricao.pago:
        inscricao.pago = True

        # Solução para somar 30 dias corridos
        inscricao.data_pagamento += timezone.timedelta(days=30)

        # Solução para dia fixo de pagamento
        # data_vencimento = aluguel.data_vencimento
        # if data_vencimento.month == 12: # Se for dezembro, o próximo mês é janeiro do próximo ano
        #    nova_data_vencimento = data_vencimento.replace(year=data_vencimento.year + 1, month=1)
        # else:
        #    nova_data_vencimento = data_vencimento.replace(month=data_vencimento.month + 1)

        # aluguel.data_vencimento = nova_data_vencimento

        inscricao.save()

        email = inscricao.participante.email
        assunto = 'Confirmação de pagamento recebido'
        mensagem_html = render_to_string('email/contato_evento.html', {
            'titulo_email': 'Contato Sobre Evento',
            'content': f'<p>Olá, {inscricao.participante.nome}, confirmamos o recebimento do pagamento de R$ {inscricao.valor} referente a inscrição no evento.</p>'
        })

        envia_email(email, assunto, mensagem_html)

        messages.success(request, "Pagamento registrado com sucesso.")

    return redirect('listar_inscricoes')


def contato_evento(request):
    try:
        if request.method == 'POST':
            nome = request.POST.get('nome')
            email = request.POST.get('email')
            telefone = request.POST.get('telefone')
            mensagem = request.POST.get('mensagem')
            identificador = request.POST.get('identificador')
            assunto = f'Interesse sobre o Evento - {identificador}'
            ano_atual = datetime.datetime.now().year

            mensagem_html = render_to_string('email/contato_imovel.html', {
                'titulo_email': 'Contato Sobre Evento',
                'content':
                    f'''<p>Olá, o {nome} está interessado no evento {identificador}</p>
                        <p><strong>Telefone:</strong> {telefone}</p>
                        <p><strong>E-mail:</strong> {email}</p>
                        <br>
                        <p><strong>Mensagem do contato:</strong> {mensagem}</p>''',
                'ano_atual': ano_atual
            })

            envia_email(email, assunto, mensagem_html)

            return redirect('detalhar_evento', evento_id=request.POST.get('evento_id'))
    except Exception as e:
        print(f"Ocorreu um erro ao tentar enviar o email. Erro: {e}")


def envia_email(email, assunto, mensagem_html):
    plain_message = strip_tags(mensagem_html)
    enviar_email(
        destinatario=email,
        assunto=assunto,
        mensagem=plain_message,
        mensagem_html=mensagem_html
    )

    @login_required
    def list_conferencia(request):
        conferencias = Conferencia.objects.all()
        return render(request, 'conferencias/list_conferencia', {'conferencias': conferencias})

    @login_required
    def list_palestra(request):
        palestras = Palestra.objects.all()
        return render(request, 'palestras/list_palestra', {'palestras': palestras})

    @login_required
    def list_workshop(request):
        workshops = Workshop.objects.all()
        return render(request, 'workshops/list_workshop', {'workshops': workshops})
