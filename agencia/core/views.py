from django.db import connection
from django.contrib import messages #import messages

import json
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets
from core.serializers import (
    CidadeSerializer,
    BilheteSerializer,
    ClienteSerializer,
    ComprovanteSerializer,
    DirigeSerializer,
    FuncionarioSerializer,
    IncluiSerializer,
    ItinerarioSerializer,
    OnibusSerializer,
    TelefoneCSerializer,
    TelefoneFSerializer,
)
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

from rest_framework.response import Response
from django.shortcuts import render, HttpResponse, redirect

from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView
from django.db import IntegrityError

def main(request):
    return render(request, 'core/index.html')


class ClienteCadastro(TemplateView):

    template_name = "core/cadastrocliente.html"

    def post(self, request):
        if request.POST:
            nome = request.POST.get("nome")
            email = request.POST.get("email")
            cpf = request.POST.get("cpf")
            genero = request.POST.get("genero")
            cidade = request.POST.get("cidade")
            endereco = request.POST.get("endereco")
            Cliente.objects.create(cpf_c=cpf, nome=nome, rua=endereco, cidade=cidade, email=email, sexo=genero
            )
        return redirect("/main")

class VerItinerarios(TemplateView):

    template_name = "core/verlinhas.html"

    def post(self, request):
        if request.POST:
            origem = request.POST.get("origem")
            destino = request.POST.get("destino")
            hora = request.POST.get("hora")
            a=Itinerario.objects.filter(cep_origem=origem, cep_destino=destino, hora_saida=hora)
            print(a)
            cidade_origem = Cidades.objects.filter(cep=origem)
            cidade_destino = Cidades.objects.filter(cep=destino)
            cidade_destino = cidade_destino[0].nome_cidade
            cidade_origem=cidade_origem[0].nome_cidade


        return render(request, "core/display.html", {"itinerarios": a, "origem":cidade_origem, "destino": cidade_destino})

class ComprarBilhete(TemplateView):
    template_name = 'core/comprar_bilhete.html'

    def post(self, request):
        if request.POST:
            i = Itinerario.objects.filter(num_iti=request.POST['num_iti'])
            valor = i[0].valor
            import random
            num_comprovante = random.randint(0,1000000000)
            num_bilhete = random.randint(0,1000000000)
            try:
                Bilhete.objects.create(numerobilhete=num_bilhete, numcomprovante=num_comprovante, 
                    cpf_c=request.POST['cpf'], numeropoltrona=request.POST['poltrona'], valor=valor, num_iti=request.POST['num_iti'])
                messages.success(request, "Comprada." )
                comprov = Comprovante.objects.filter(numcomprovante=num_comprovante)
                comprovante = {"numero": comprov[0].numcomprovante, "cpf": comprov[0].cpf_c, "valor":comprov[0].valor}
                print(comprovante)
                return render(request, 'core/index.html', comprovante)
            except IntegrityError:
                messages.error(request, 'Poltrona não está livre, tente outra')
                return render(request, 'core/index.html')





































class BilheteViewSet(viewsets.ModelViewSet):
    serializer_class = BilheteSerializer
    queryset = Bilhete.objects.all()


class CidadeViewSet(viewsets.ModelViewSet):
    serializer_class = CidadeSerializer
    queryset = Cidades.objects.all()


class ClienteViewSet(viewsets.ModelViewSet):
    serializer_class = ClienteSerializer
    queryset = Cliente.objects.all()

    @action(methods=["GET"], detail=False)
    def telefones(self, request, pk=None):
        #Consulta 3.2.4
        if request.method == "GET":
            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT nome, telefone 

                        FROM cliente AS c 

                        INNER JOIN telefone_c AS t_c 

                        ON c.cpf_c = t_c.cpf_c """
                )

                columns = [col[0] for col in cursor.description]
                return Response([dict(zip(columns, row)) for row in cursor.fetchall()])
    @action(methods=["POST"], detail=False)
    def buscar_por_hora(self, request, pk=None):
        #Consulta 3.2.1
        if request.method == "POST":
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT nome FROM passagens_compradas AS cli, itinerario AS iti
WHERE cli.num_iti = iti.num_iti
AND hora_saida = '{request.data['horario']}'
                    """)
                columns = [col[0] for col in cursor.description]
                return Response([dict(zip(columns, row)) for row in cursor.fetchall()])


class ComprovanteViewSet(viewsets.ModelViewSet):
    serializer_class = ComprovanteSerializer
    queryset = Comprovante.objects.all()


class DirigeViewSet(viewsets.ModelViewSet):
    serializer_class = DirigeSerializer
    queryset = Dirige.objects.all()


class FuncionarioViewSet(viewsets.ModelViewSet):
    serializer_class = FuncionarioSerializer
    queryset = Funcionario.objects.all()

    @action(methods=["POST"], detail=False)
    def motorista(self, request, pk=None):
        """Consulta 3.22"""
        if request.method == "POST":
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT nome FROM funcionario 
                                WHERE cpf_f IN (SELECT cpf_f FROM dirige  

                                    WHERE numonibus IN (SELECT numonibus FROM onibus  

                                        WHERE numitipercorre IN (SELECT num_iti FROM itinerario  

                                            WHERE cep_origem IN (SELECT cep FROM cidades  

                                                WHERE nome_cidade LIKE '%{request.data['origem']}') 

                                            AND cep_destino IN (SELECT cep FROM cidades  

                                                WHERE nome_cidade LIKE '%{request.data['destino']}')))) """)
                columns = [col[0] for col in cursor.description]
                return Response([dict(zip(columns, row)) for row in cursor.fetchall()])
    @action(methods=["POST"], detail=False)
    def buscar_vendedor(self, request, pk=None):
        #Consulta 3.2.3
        if request.method == "POST":
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    SELECT DISTINCT nome, numvendas FROM funcionario as f 
                    WHERE idvendedor IN (SELECT idvendedor FROM comprovante  
                    WHERE cpf_c IN (SELECT cpf_c FROM cliente 
                    WHERE nome = '{request.data['cliente']}')) """)

                columns = [col[0] for col in cursor.description]
                return Response([dict(zip(columns, row)) for row in cursor.fetchall()])

    @action(methods=["GET"], detail=False)
    def tipos(self, request, pk=None):
        #Consula 3.2.6
        if request.method == "GET":
            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT tipo, COUNT(tipo)
                        FROM funcionario 
                        GROUP BY tipo """
                )
                columns = [col[0] for col in cursor.description]
                return Response([dict(zip(columns, row)) for row in cursor.fetchall()])


class IncluiViewSet(viewsets.ModelViewSet):
    serializer_class = IncluiSerializer
    queryset = Inclui.objects.all()


class ItinerarioViewSet(viewsets.ModelViewSet):
    serializer_class = ItinerarioSerializer
    queryset = Itinerario.objects.all()

    @action(methods=["GET"], detail=False)
    def barato(self, request, pk=None):
        #Consulta 3.2.8
        if request.method == "GET":
            query = Itinerario.objects.raw(
                "SELECT num_iti, valor FROM Itinerario ORDER BY valor ASC"
            )
            dicionario = {"itinerarios": []}
            for i in query:
                dicionario["itinerarios"].append(
                    {"num_iti": i.num_iti, "valor": i.valor}
                )
            return Response(dicionario)

    @action( methods=["POST"], detail=False)
    def ceps(self, request, pk=None):
        #Consulta 3.2.7
        if request.method == "POST":
            print(request.data)
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    SELECT num_iti, cep_origem, cep_destino FROM itinerario 
                    
                    WHERE cep_origem = %s AND cep_destino = %s
                    """, [request.data['origem'], request.data['destino']]                )
                columns = [col[0] for col in cursor.description]
                return Response([dict(zip(columns, row)) for row in cursor.fetchall()])


class OnibusViewSet(viewsets.ModelViewSet):
    serializer_class = OnibusSerializer
    queryset = Onibus.objects.all()

class TelefoneCViewSet(viewsets.ModelViewSet):
    serializer_class = TelefoneCSerializer
    queryset = TelefoneC.objects.all()


class TelefoneFViewSet(viewsets.ModelViewSet):
    serializer_class = TelefoneFSerializer
    queryset = TelefoneF.objects.all()
