from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Cliente, Mascota
from .serializers import ClienteSerializer, MascotaSerializer
from .models import Especie
from .serializers import EspecieSerializer
from .models import Direccion
from .serializers import DireccionSerializer

class DireccionViewSet(viewsets.ModelViewSet):
    queryset = Direccion.objects.all()
    serializer_class = DireccionSerializer

class EspecieViewSet(viewsets.ModelViewSet):
    queryset = Especie.objects.all()
    serializer_class = EspecieSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['activo', 'genero']
    search_fields = ['nombre', 'apellido', 'email']
    ordering_fields = ['nombre', 'apellido', 'fecha_registro']


class MascotaViewSet(viewsets.ModelViewSet):
    queryset = Mascota.objects.all()
    serializer_class = MascotaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['especie', 'sexo', 'esterilizado']
    search_fields = ['nombre']
    ordering_fields = ['nombre', 'fecha_registro']