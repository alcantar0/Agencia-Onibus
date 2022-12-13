from rest_framework import serializers
from core.models import (
    Cidades,
    Bilhete,
    Cliente,
    Comprovante,
    Dirige,
    Funcionario,
    Inclui,
    Itinerario,
    Onibus,
    TelefoneC,
    TelefoneF,
)


class BilheteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bilhete
        queryset = Bilhete.objects.all()
        fields = "__all__"


class CidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cidades
        queryset = Cidades.objects.all()
        fields = "__all__"


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        queryset = Cliente.objects.all()
        fields = "__all__"


class ComprovanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comprovante
        queryset = Comprovante.objects.all()
        fields = "__all__"


class DirigeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dirige
        queryset = Dirige.objects.all()
        fields = "__all__"


class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        queryset = Funcionario.objects.all()
        fields = "__all__"


class IncluiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inclui
        queryset = Inclui.objects.all()
        fields = "__all__"


class ItinerarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Itinerario
        queryset = Itinerario.objects.all()
        fields = "__all__"


class OnibusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Onibus
        queryset = Onibus.objects.all()
        fields = "__all__"


class TelefoneCSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelefoneC
        queryset = TelefoneC.objects.all()
        fields = "__all__"


class TelefoneFSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelefoneF
        queryset = TelefoneF.objects.all()
        fields = "__all__"
