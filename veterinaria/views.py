from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Cita
from .serializers import CitaSerializer


class CitaViewSet(viewsets.ModelViewSet):
    queryset = Cita.objects.all()
    serializer_class = CitaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['estado', 'veterinario']
    search_fields = ['mascota__nombre']
    ordering_fields = ['fecha_hora']