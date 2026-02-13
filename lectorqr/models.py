from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator
from .fields import EncryptedTextField

# =========================
# VALIDADOR ALFANUMÉRICO
# =========================
alphanumeric_10 = RegexValidator(
    regex=r'^[A-Za-z0-9]{1,10}$',
    message='El ID debe ser alfanumérico y tener máximo 10 caracteres.'
)


# =========================
# MODELO PACIENTE
# =========================
class Paciente(models.Model):

    # 🔑 LLAVE PRIMARIA AUTOINCREMENTAL
    codigo = models.BigAutoField(
        primary_key=True,
        verbose_name="Código interno"
    )

    # 🆔 ID ALFANUMÉRICO (QR)
    id = models.CharField(
        max_length=10,
        unique=True,
        validators=[alphanumeric_10],
        verbose_name="ID QR"
    )

    # 🔐 CAMPOS CIFRADOS
    nombre = EncryptedTextField(verbose_name="Nombre")

    # 🧮 EDAD (NO CIFRADA)
    edad = models.PositiveIntegerField(
        verbose_name="Edad"
    )

    # 🚻 SEXO
    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    )

    sexo = models.CharField(
        max_length=1,
        choices=SEXO_CHOICES,
        verbose_name="Sexo"
    )

    # email REMOVIDO
    
    telefono = EncryptedTextField(verbose_name="Teléfono", null=True, blank=True)
    
    # Renombrado de 'texto' a 'datos_medico'
    datos_medico = EncryptedTextField(verbose_name="Datos del médico")

    # Campos nuevos
    informacion_clinica = EncryptedTextField(verbose_name="Información clínica", default="")
    resultado_prueba = EncryptedTextField(verbose_name="Resultado de la prueba", default="")

    # 📅 FECHA DE REGISTRO (NO CIFRADA)
    fecha_de_registro = models.DateField(
        auto_now_add=True,
        verbose_name="Fecha de registro"
    )

    # 📷 IMÁGENES (NO CIFRADAS)
    foto_perfil = models.ImageField(
        upload_to='images/perfil/',
        null=True,
        blank=True
    )

    foto_resultado = models.ImageField(
        upload_to='results/resultado/',
        null=True,
        blank=True
    )

    # 👤 REGISTRADO POR (Campo automático)
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pacientes_registrados',
        verbose_name="Registrado por"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} ({self.codigo})"

    class Meta:
        db_table = "pacientes"
        ordering = ["-codigo"]


# =========================
# REGISTRO DE ESCANEOS
# =========================
class ScanLog(models.Model):

    scanner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='scan_logs',
        verbose_name="Escaneado por"
    )

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='scan_logs',
        verbose_name="Paciente Escaneado"
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha y Hora"
    )

    class Meta:
        verbose_name = "Registro de Escaneo"
        verbose_name_plural = "Registros de Escaneos"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.scanner.username} escaneó a {self.paciente.id} el {self.timestamp}"
