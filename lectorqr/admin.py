from django.contrib import admin
from .models import Paciente, ScanLog

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    readonly_fields = ('registrado_por',)
    list_display = ('id', 'nombre', 'fecha_de_registro', 'registrado_por')
    search_fields = ('id', 'nombre', 'registrado_por__username')

@admin.register(ScanLog)
class ScanLogAdmin(admin.ModelAdmin):
    list_display = ('scanner', 'paciente', 'timestamp')
    list_filter = ('timestamp', 'scanner')
    search_fields = ('scanner__username', 'paciente__id', 'paciente__nombre')
