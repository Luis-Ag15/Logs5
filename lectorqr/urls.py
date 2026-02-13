from django.urls import path
from . import views
from .views import ScannerPageView, PacienteCreateView

urlpatterns = [

    path('scanner/', ScannerPageView.as_view(), name='scanner'),
    path('buscar-paciente/', views.view_detalles_paciente, name='view_detalles_paciente'),
    path('detalles-busqueda/', views.detalles_paciente, name='detalles_paciente'),
    path('resultados/', PacienteCreateView.as_view(), name='paciente_create'),

]

