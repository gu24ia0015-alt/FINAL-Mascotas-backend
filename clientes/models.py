from django.db import models


class Cliente(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    dni = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Direccion(models.Model):
    TIPO_CHOICES = [
        ('envio', 'Envío'),
        ('facturacion', 'Facturación'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='direcciones')
    calle = models.CharField(max_length=150)
    numero = models.CharField(max_length=10)
    colonia = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10)
    pais = models.CharField(max_length=100, default='México')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='envio')
    principal = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.calle} {self.numero}, {self.ciudad}"


class Especie(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "Especies"

    def __str__(self):
        return self.nombre


class Raza(models.Model):
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE, related_name='razas')
    nombre = models.CharField(max_length=100)
    tamano_promedio = models.CharField(max_length=50, blank=True)
    esperanza_vida_anios = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Razas"

    def __str__(self):
        return self.nombre


class Mascota(models.Model):
    SEXO_CHOICES = [
        ('M', 'Macho'),
        ('H', 'Hembra'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='mascotas')
    especie = models.ForeignKey(Especie, on_delete=models.PROTECT)
    raza = models.ForeignKey(Raza, on_delete=models.PROTECT, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    color = models.CharField(max_length=50, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    esterilizado = models.BooleanField(default=False)
    foto_url = models.URLField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    notas = models.TextField(blank=True)

    def __str__(self):
        return self.nombre