from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView
from django.http import JsonResponse
from django.contrib import messages

from . import models
from .models import Paciente
from .forms import PacienteForm


# ======================================================
# REGISTRO DE RESULTADOS (SOLO STAFF Y SUPERUSERS)
# ======================================================
class PacienteCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'lectorqr/paciente_form.html'
    login_url = reverse_lazy('login')

    # 🔐 Validación de permisos (SOLO STAFF / SUPERUSER)
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def form_valid(self, form):
        form.instance.registrado_por = self.request.user
        self.object = form.save()
        messages.success(
            self.request,
            "Resultados registrados exitosamente"
        )
        return redirect('paciente_create')


# ======================================================
# PÁGINA DEL SCANNER (TODOS LOS USUARIOS AUTENTICADOS)
# ======================================================
class ScannerPageView(LoginRequiredMixin, TemplateView):
    template_name = "lectorqr/scanner.html"
    login_url = reverse_lazy('login')


# ======================================================
# CONSULTA POR QR (TODOS LOS USUARIOS AUTENTICADOS)
# ======================================================
def view_detalles_paciente(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Acceso no autorizado'}, status=403)

    if request.method == 'POST':
        result_qr = request.POST.get('datoqr')

        try:
            pacienteBD = models.Paciente.objects.get(id=result_qr)
            
            # 📜 REGISTRAR EL ESCANEO
            models.ScanLog.objects.create(
                scanner=request.user,
                paciente=pacienteBD
            )
            
            return JsonResponse({'id_paciente': pacienteBD.id})

        except models.Paciente.DoesNotExist:
            return JsonResponse({'id_paciente': 0})

    return JsonResponse({'error': 'Solicitud no válida'}, status=400)


# ======================================================
# DETALLES DEL ALUMNO (TODOS LOS USUARIOS AUTENTICADOS)
# ======================================================
def detalles_paciente(request):
    if not request.user.is_authenticated:
        return redirect('login')

    id_paciente = request.GET.get('id')

    if id_paciente:
        try:
            paciente = models.Paciente.objects.get(id=id_paciente)
            return render(
                request,
                "lectorqr/detalles_busqueda.html",
                {"paciente": paciente}
            )

        except models.Paciente.DoesNotExist:
            return render(
                request,
                "error.html",
                {
                    "error_message": (
                        f"No existe ningún registro para el ID de paciente: {id_paciente}"
                    )
                }
            )

    return JsonResponse(
        {"error": "No se proporcionó el parámetro 'id' en la URL."},
        status=400
    )


