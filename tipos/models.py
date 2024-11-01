from django.db import models


# Modelo para os Tipos de eventos
class Conferencia(models.Model):
    nome_do_evento = models.CharField(max_length=100)
    data_inicio = models.DateField(max_length=15)
    hora_inicio = models.TimeField(max_length=15)
    data_final = models.DateField(max_length=15)
    hora_final = models.TimeField(max_length=15)
    endereco = models.CharField(max_length=255)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    email_contato = models.EmailField(max_length=50)
    valor_inscricao = models.DecimalField(max_digits=8, decimal_places=2)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nome_do_evento} - {self.data_inicio}/{self.data_final}"

# Modelo para Partcicipantes
class Participante(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    nome_do_evento = models.ForeignKey(Conferencia, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome} - {self.nome_do_evento.nome_do_evento}"


