from django.contrib import admin
from .models import Cliente, Servicio

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio", "duracion_min")
    search_fields = ("nombre",)
    ordering = ("duracion_min",)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "telefono", )
    search_fields = ("nombre",)
    ordering = ("nombre",)