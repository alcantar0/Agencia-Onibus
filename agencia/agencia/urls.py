"""agencia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from django.urls import include, path
from core import views
from core.views import (
    CidadeViewSet,
    BilheteViewSet,
    ClienteViewSet,
    ComprovanteViewSet,
    DirigeViewSet,
    FuncionarioViewSet,
    IncluiViewSet,
    ItinerarioViewSet,
    OnibusViewSet,
    TelefoneCViewSet,
    TelefoneFViewSet,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerSplitView

router = routers.DefaultRouter()

router.register(r"cidades", CidadeViewSet, basename="cidades")

router.register(r"bilhetes", BilheteViewSet, basename="bilhetes")

router.register(r"clientes", ClienteViewSet, basename="clientes")

router.register(r"comprovantes", ComprovanteViewSet, basename="comprovantes")

router.register(r"dirige", DirigeViewSet, basename="dirige")

router.register(r"funcionarios", FuncionarioViewSet, basename="funcionarios")

router.register(r"inclui", IncluiViewSet, basename="inclui")

router.register(r"itinerarios", ItinerarioViewSet, basename="itinerarios")

router.register(r"onibus", OnibusViewSet, basename="onibus")

router.register(r"telefones_c", TelefoneCViewSet, basename="telefones_c")

router.register(r"telefones_f", TelefoneFViewSet, basename="telefones_f")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/openapi/",
        SpectacularSwaggerSplitView.as_view(url_name="schema"),
        name="openapi",
    ),
    path("", views.main),
    path('cliente/', views.ClienteCadastro.as_view()),
    path('itinerarios/', views.VerItinerarios.as_view()),
    path("itinerarios/comprar/", views.ComprarBilhete.as_view()),

    ]
