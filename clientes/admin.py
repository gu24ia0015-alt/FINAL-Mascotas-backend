from django.contrib import admin
from .models import Cliente, Direccion, Especie, Raza, Mascota


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'telefono', 'activo', 'fecha_registro')
    list_filter = ('activo', 'genero', 'fecha_registro')
    search_fields = ('nombre', 'apellido', 'email', 'dni')
    ordering = ('apellido', 'nombre')


@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'calle', 'ciudad', 'estado', 'tipo', 'principal')
    list_filter = ('tipo', 'estado', 'principal')
    search_fields = ('cliente__nombre', 'cliente__apellido', 'ciudad')
    ordering = ('cliente',)


@admin.register(Especie)
class EspecieAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    ordering = ('nombre',)


@admin.register(Raza)
class RazaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especie', 'tamano_promedio', 'esperanza_vida_anios')
    list_filter = ('especie',)
    search_fields = ('nombre',)
    ordering = ('especie', 'nombre')


@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cliente', 'especie', 'raza', 'sexo', 'esterilizado', 'fecha_registro')
    list_filter = ('especie', 'sexo', 'esterilizado')
    search_fields = ('nombre', 'cliente__nombre', 'cliente__apellido')
    ordering = ('nombre',)