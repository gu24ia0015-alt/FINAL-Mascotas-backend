from django.contrib import admin
from .models import (
    Categoria, Proveedor, Producto, Cupon, Carrito,
    CarritoItem, Pedido, DetallePedido, Pago, Resena
)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria_padre')
    list_filter = ('categoria_padre',)
    search_fields = ('nombre',)
    ordering = ('nombre',)


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'contacto', 'telefono', 'email', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre', 'contacto', 'email')
    ordering = ('nombre',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sku', 'categoria', 'precio', 'stock', 'activo')
    list_filter = ('categoria', 'proveedor', 'activo')
    search_fields = ('nombre', 'sku', 'marca')
    ordering = ('nombre',)


@admin.register(Cupon)
class CuponAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'tipo_descuento', 'valor', 'fecha_inicio', 'fecha_fin', 'activo')
    list_filter = ('tipo_descuento', 'activo')
    search_fields = ('codigo',)
    ordering = ('-fecha_inicio',)


class CarritoItemInline(admin.TabularInline):
    model = CarritoItem
    extra = 1


@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'estado', 'fecha_creacion')
    list_filter = ('estado',)
    search_fields = ('cliente__nombre', 'cliente__apellido')
    ordering = ('-fecha_creacion',)
    inlines = [CarritoItemInline]


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 1


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'estado', 'total', 'fecha_pedido')
    list_filter = ('estado', 'metodo_pago')
    search_fields = ('cliente__nombre', 'cliente__apellido')
    ordering = ('-fecha_pedido',)
    inlines = [DetallePedidoInline]


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido', 'monto', 'metodo', 'estado', 'fecha_pago')
    list_filter = ('estado', 'metodo')
    search_fields = ('pedido__id', 'referencia_transaccion')
    ordering = ('-fecha_pago',)


@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'producto', 'calificacion', 'fecha')
    list_filter = ('calificacion',)
    search_fields = ('cliente__nombre', 'producto__nombre')
    ordering = ('-fecha',)