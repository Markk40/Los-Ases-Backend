from rest_framework import serializers
from .models import Categoria, Subasta, Puja

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class SubastaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subasta
        fields = '__all__'

class PujaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Puja
        fields = '__all__'
