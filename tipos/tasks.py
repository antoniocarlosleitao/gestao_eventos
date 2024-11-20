from celery import shared_task
import datetime
from datetime import timedelta
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from gestao_eventos.utils import enviar_email
from tipos.models import Evento
import logging

logger = logging.getLogger(__name__)

@shared_task
def verificar_data_inicio():
    try:
        hoje = datetime.date.today()
        data_inicio_proximo = hoje + timedelta(days=7)

        # Filtra insrcrições a vencer em 7 dias que ainda estão com pagamento em aberto
        inscricoes_a_vencer = Evento.objects.filter(
            Q(pago=False) &
            Q(data_vencimento__lte=data_inicio_proximo) &
            Q(data_vencimento__gte=hoje)
        )

        # Filtra pagamento de inscrição vencido e ainda não pagos
        pagamento_de_inscricao_vencido = Evento.objects.filter(
            Q(pago=False) &
            Q(data_vencimento__lt=hoje)
        )

        logger.info(f"Inscrições a vencer: {inscricoes_a_vencer.count()}")
        logger.info(f"Inscrições vencidas: {pagamento_de_inscricao_vencido.count()}")

        # Envia notificações para inscrições a vencer
        for inscricao in inscricoes_a_vencer:
            envia_email_notificacao(inscricao, 'proximo_vencimento')

        # Envia notificações para aluguéis vencidos
        for inscricao in pagamento_de_inscricao_vencido:
            envia_email_notificacao(inscricao, 'vencido')

    except Exception as e:
        logger.error(f"Erro na task de data_inicio: {e}")

def envia_email_notificacao(inscricao, tipo):
    if tipo == 'proximo_vencimento':
        assunto = f'Lembrete: Sua inscrição vence em breve'
        template_content = 'email/proximo_vencimento.html'
    else:
        assunto = 'Aviso: Sua inscrição expirou!'
        template_content = 'email/inscricao_vencido.html'

    mensagem_html = render_to_string(template_content, {
        'inscricao': inscricao,
        'titulo_email': assunto,
        'ano_atual': datetime.datetime.now().year
    })

    plain_message = strip_tags(mensagem_html)

    enviar_email(
        destinatario=inscricao.participante.email,
        assunto=assunto,
        mensagem=plain_message,
        mensagem_html=mensagem_html
    )