from django.contrib import messages #import messages

import json
from django.shortcuts import render

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
            #Recebe os dados dos forms
            nome = request.POST.get("nome")
            email = request.POST.get("email")
            cpf = request.POST.get("cpf")
            genero = request.POST.get("genero")
            cidade = request.POST.get("cidade")
            endereco = request.POST.get("endereco")
            try:
                Cliente.objects.create(cpf_c=cpf, nome=nome, rua=endereco, cidade=cidade, email=email, sexo=genero
                )
                messages.success(request, "Cliente cadastrado!" )
                return render(request, 'core/index.html')
            except IntegrityError:
                messages.error(request, 'Cliente já existe!')
                return render(request, 'core/index.html')

class VerItinerarios(TemplateView):

    template_name = "core/verlinhas.html"

    def post(self, request):
        if request.POST:
            #Recebe os dados do formulário
            origem = request.POST.get("origem")
            destino = request.POST.get("destino")
            hora = request.POST.get("hora")
            #Busca o itineráio com esses dados
            a=Itinerario.objects.filter(cep_origem=origem, cep_destino=destino, hora_saida=hora)
            cidade_origem = Cidades.objects.filter(cep=origem)
            cidade_destino = Cidades.objects.filter(cep=destino)
            cidade_destino = cidade_destino[0].nome_cidade
            cidade_origem=cidade_origem[0].nome_cidade


        return render(request, "core/display.html", {"itinerarios": a, "origem":cidade_origem, "destino": cidade_destino})

class ComprarBilhete(TemplateView):
    template_name = 'core/comprar_bilhete.html'

    def post(self, request):
        if request.POST:
            #Busca o itineráio com esse esse num_iti
            i = Itinerario.objects.filter(num_iti=request.POST['num_iti'])
            valor = i[0].valor
            import random
            num_comprovante = random.randint(0,1000000000)
            num_bilhete = random.randint(0,1000000000)
            try:
                #Cria o objeto Bilhete, por consequência é criado uma linha na tabela comprovante por conta da trigger criada na etapa 7
                Bilhete.objects.create(numerobilhete=num_bilhete, numcomprovante=num_comprovante, 
                    cpf_c=request.POST['cpf'], numeropoltrona=request.POST['poltrona'], valor=valor, num_iti=request.POST['num_iti'])
                messages.success(request, "Comprada." )
                comprov = Comprovante.objects.filter(numcomprovante=num_comprovante)
                comprovante = {"numero": comprov[0].numcomprovante, "cpf": comprov[0].cpf_c, "valor":comprov[0].valor}
                return render(request, 'core/index.html', comprovante)
            except IntegrityError:#Pega o erro caso a poltrona já esteja ocupada
                messages.error(request, 'Poltrona não está livre, tente outra')
                return render(request, 'core/index.html')





































