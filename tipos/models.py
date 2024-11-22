from django.db import models
from decimal import Decimal
import random

TIPO_EVENTO_CHOICES = [
    ('CON', 'Conferencia'),
    ('PLA', 'Palestra'),
    ('WKS', 'Workshop'),
]

# Modelo para os Tipos de eventos
class Evento(models.Model):
    identificador = models.CharField(max_length=10, unique=True)
    nome_do_evento = models.CharField(max_length=100)
    data_inicio = models.DateField(max_length=15)
    hora_inicio = models.TimeField(max_length=15)
    data_final = models.DateField(max_length=15)
    hora_final = models.TimeField(max_length=15)
    cep = models.CharField(max_length=10)
    endereco = models.CharField(max_length=255)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    email_contato = models.EmailField(max_length=50)
    valor_inscricao = models.DecimalField(max_digits=8, decimal_places=2)
    descricao = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.identificador:
            while True:
                prefixo = self.nome_do_evento
                sufixo = str(random.randint(10000, 99999))
                identificador = f"{prefixo}-{sufixo}"
                if not Evento.objects.filter(identificador=identificador).exists():
                    self.identificador = identificador
                    break;
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.identificador}"
# Modelo para as imagens do Evento
class ImagemEvento(models.Model):
    evento = models.ForeignKey(Evento, related_name='imagens', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='tipos/')
    destaque = models.BooleanField(default=False)
    data_upload = models.DateTimeField(auto_now_add=True)

# Modelo para Partcicipantes
class Participante(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=20)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    nome_do_evento = models.ForeignKey(Evento, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome} - {self.nome_do_evento.nome_do_evento} - {self.telefone} - {self.email}"


# Modelo para Inscrição
class Inscricao(models.Model):
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    data_pagamento = models.DateField()
    valor_inscricao = models.DecimalField(max_digits=10, decimal_places=2)
    pago = models.BooleanField(default=False)
    material = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.0'), blank=True, null=True)
    almoco = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.0'), blank=True, null=True)
    certificado = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.0'), blank=True, null=True)
    outras_taxas = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.0'), blank=True, null=True)

    def save(self, *args, **kwargs):
        # Calcula o valor total considerando o preço do aluguel e as taxas
        valor_inscricao = self.evento.valor_inscricao if self.evento else Decimal('0.0')
        self.valor_inscricao = valor_inscricao + (self.material or Decimal('0.0')) + (self.almoco or Decimal('0.0')) + \
                     (self.certificado or Decimal('0.0')) + (self.outras_taxas or Decimal('0.0'))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Inscrição de {self.participante.nome} - {self.evento.nome_do_evento} - {self.data_pagamento} - R$ {self.valor_inscricao}"