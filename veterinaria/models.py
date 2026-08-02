from django.db import models
from clientes.models import Mascota, Cliente


class Veterinario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula_profesional = models.CharField(max_length=30, unique=True)
    especialidad = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    fecha_contratacion = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Dr(a). {self.nombre} {self.apellido}"


class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    duracion_minutos = models.PositiveIntegerField(default=30)
    categoria = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.nombre


class Cita(models.Model):
    ESTADO_CHOICES = [
        ('agendada', 'Agendada'),
        ('confirmada', 'Confirmada'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]

    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='citas')
    veterinario = models.ForeignKey(Veterinario, on_delete=models.PROTECT, related_name='citas')
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT)
    fecha_hora = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='agendada')
    motivo = models.CharField(max_length=200, blank=True)
    notas = models.TextField(blank=True)
    costo = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Citas"

    def __str__(self):
        return f"{self.mascota} - {self.fecha_hora:%Y-%m-%d %H:%M}"


class HistorialMedico(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='historial_medico')
    cita = models.ForeignKey(Cita, on_delete=models.SET_NULL, null=True, blank=True, related_name='historial')
    veterinario = models.ForeignKey(Veterinario, on_delete=models.PROTECT)
    fecha = models.DateField(auto_now_add=True)
    diagnostico = models.TextField()
    tratamiento = models.TextField(blank=True)
    peso_registrado = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    observaciones = models.TextField(blank=True)
    proxima_revision = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Historiales médicos"
        verbose_name = "Historial médico"

    def __str__(self):
        return f"Historial de {self.mascota} - {self.fecha}"


class Vacuna(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='vacunas')
    veterinario = models.ForeignKey(Veterinario, on_delete=models.PROTECT)
    nombre_vacuna = models.CharField(max_length=100)
    fecha_aplicacion = models.DateField()
    lote = models.CharField(max_length=50, blank=True)
    fecha_proxima_dosis = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre_vacuna} - {self.mascota}"


class Refugio(models.Model):
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    capacidad = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.nombre


class Adopcion(models.Model):
    ESTADO_CHOICES = [
        ('en_proceso', 'En proceso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]

    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='adopciones')
    refugio = models.ForeignKey(Refugio, on_delete=models.SET_NULL, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='adopciones')
    fecha_adopcion = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='en_proceso')
    costo_adopcion = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    contrato_firmado = models.BooleanField(default=False)

    def __str__(self):
        return f"Adopción de {self.mascota} por {self.cliente}"