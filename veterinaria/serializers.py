from rest_framework import serializers
from .models import Cita


class CitaSerializer(serializers.ModelSerializer):
    mascota_nombre = serializers.CharField(source='mascota.nombre', read_only=True)
    veterinario_nombre = serializers.CharField(source='veterinario.nombre', read_only=True)
    servicio_nombre = serializers.CharField(source='servicio.nombre', read_only=True)

    class Meta:
        model = Cita
        fields = '__all__'