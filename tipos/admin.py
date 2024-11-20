from django.contrib import admin
from tipos.models import Evento, Participante, Inscricao

# Register your models here.
admin.site.register(Evento)
admin.site.register(Participante)
admin.site.register(Inscricao)