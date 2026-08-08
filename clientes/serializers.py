from rest_framework import serializers
from .models import Cliente, Mascota
from .models import Especie
from .models import Direccion

class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = '__all__'

class EspecieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especie
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'


class MascotaSerializer(serializers.ModelSerializer):
    especie_nombre = serializers.CharField(source='especie.nombre', read_only=True)
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)

    class Meta:
        model = Mascota
        fields = '__all__'