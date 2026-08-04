from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Producto, Pedido
from .serializers import ProductoSerializer, PedidoSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'proveedor', 'activo']
    search_fields = ['nombre', 'sku', 'marca']
    ordering_fields = ['nombre', 'precio', 'stock']


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['estado', 'cliente']
    search_fields = ['cliente__nombre', 'cliente__apellido']
    ordering_fields = ['fecha_pedido', 'total']