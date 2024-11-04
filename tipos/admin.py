from django.contrib import admin
from tipos.models import Conferencia, Palestra, Workshop

# Register your models here.
admin.site.register(Conferencia)
admin.site.register(Palestra)
admin.site.register(Workshop)