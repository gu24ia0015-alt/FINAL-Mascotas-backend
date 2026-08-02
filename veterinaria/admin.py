from django.contrib import admin
from .models import Veterinario, Servicio, Cita, HistorialMedico, Vacuna, Refugio, Adopcion


@admin.register(Veterinario)
class VeterinarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'cedula_profesional', 'especialidad')
    list_filter = ('especialidad',)
    search_fields = ('nombre', 'apellido', 'cedula_profesional')
    ordering = ('apellido',)


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'duracion_minutos', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('nombre',)
    ordering = ('nombre',)


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'veterinario', 'servicio', 'fecha_hora', 'estado')
    list_filter = ('estado', 'veterinario')
    search_fields = ('mascota__nombre', 'veterinario__nombre')
    ordering = ('-fecha_hora',)


@admin.register(HistorialMedico)
class HistorialMedicoAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'veterinario', 'fecha', 'diagnostico')
    list_filter = ('veterinario', 'fecha')
    search_fields = ('mascota__nombre', 'diagnostico')
    ordering = ('-fecha',)


@admin.register(Vacuna)
class VacunaAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'nombre_vacuna', 'fecha_aplicacion', 'fecha_proxima_dosis')
    list_filter = ('nombre_vacuna',)
    search_fields = ('mascota__nombre', 'nombre_vacuna')
    ordering = ('-fecha_aplicacion',)


@admin.register(Refugio)
class RefugioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'email', 'capacidad')
    search_fields = ('nombre',)
    ordering = ('nombre',)


@admin.register(Adopcion)
class AdopcionAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'cliente', 'refugio', 'estado', 'fecha_adopcion')
    list_filter = ('estado', 'refugio')
    search_fields = ('mascota__nombre', 'cliente__nombre')
    ordering = ('-fecha_adopcion',)