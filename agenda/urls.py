"""
URL configuration for agenda project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from citas import views


urlpatterns = [
    path("admin/", admin.site.urls),

    path("servicios/iva/", views.servicios_iva),

    path("cita/<int:numero>/pagado/", views.cita_pagado),

    path("servicios/", views.lista_servicios),

    path("servicios/resumen/", views.resumen_servicios),

    path("citas/", views.lista_citas),

    path("citas/ingresos/", views.ingresos_facturados),

    path("citas/pendientes/", views.citas_pendientes),

    path("servicios/economicos/", views.servicios_economicos),

    path("cita/<int:numero>/estado/", views.estado_cita),

    path("cita/<int:numero>/", views.detalle_cita),

    path("citas/duracion/", views.duracion_citas),

    path("clientes/citas/", views.citas_por_cliente),

    path("informe/", views.informe_general),

    path("servicios/populares/", views.servicios_populares),
]

