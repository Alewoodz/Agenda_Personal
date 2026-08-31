from django.http import HttpResponse
from .models import Cliente, Servicio, Cita, Pago
def servicios_iva(request):

    servicios = Servicio.objects.all()

    respuesta = "<h1>Servicios con IVA</h1>"

    for servicio in servicios:

        precio_iva = round(servicio.precio * 1.19)

        respuesta += (
            f"<p>"
            f"{servicio.nombre} - "
            f"Precio: ${servicio.precio} - "
            f"Precio con IVA: ${precio_iva}"
            f"</p>"
        )

    return HttpResponse(respuesta)

def cita_pagado(request, numero):

    try:
        cita = Cita.objects.get(id=numero)
    except Cita.DoesNotExist:
        return HttpResponse("La cita no existe.")

    total_pagado = 0

    for pago in cita.pagos.all():
        total_pagado += pago.monto

    return HttpResponse(
        f"<h1>Total pagado</h1>"
        f"<p>Cita: {cita.id}</p>"
        f"<p>Total pagado: ${total_pagado}</p>"
    )

def lista_servicios(request):

    servicios = Servicio.objects.all()

    respuesta = "<h1>Catálogo de servicios</h1>"

    for servicio in servicios:

        respuesta += (
            f"<p>"
            f"{servicio.nombre} - "
            f"${servicio.precio} - "
            f"{servicio.duracion_min} minutos"
            f"</p>"
        )

    return HttpResponse(respuesta)

def resumen_servicios(request):

    servicios = Servicio.objects.all()

    cantidad = 0
    suma_precios = 0
    precio_mayor = 0

    for servicio in servicios:

        cantidad += 1
        suma_precios += servicio.precio

        if servicio.precio > precio_mayor:
            precio_mayor = servicio.precio

    if cantidad > 0:
        promedio = suma_precios / cantidad
    else:
        promedio = 0

    return HttpResponse(
        f"<h1>Resumen de servicios</h1>"
        f"<p>Cantidad: {cantidad}</p>"
        f"<p>Precio promedio: ${round(promedio)}</p>"
        f"<p>Precio más caro: ${precio_mayor}</p>"
    )

def lista_citas(request):

    citas = Cita.objects.all()

    respuesta = "<h1>Listado de citas</h1>"

    for cita in citas:

        respuesta += (
            f"<p>"
            f"Cliente: {cita.cliente.nombre} - "
            f"Servicio: {cita.servicio.nombre} - "
            f"Estado: {cita.estado}"
            f"</p>"
        )

    return HttpResponse(respuesta)

def ingresos_facturados(request):

    citas = Cita.objects.all()

    total = 0

    for cita in citas:

        if cita.estado == "atendida":
            total += cita.servicio.precio

    return HttpResponse(
        f"<h1>Ingresos facturados</h1>"
        f"<p>Total facturado: ${total}</p>"
    )

def citas_pendientes(request):

    citas = Cita.objects.all()

    cantidad = 0
    respuesta = "<h1>Citas pendientes</h1>"

    for cita in citas:

        if cita.estado == "pendiente":

            cantidad += 1

            respuesta += (
                f"<p>"
                f"{cita.cliente.nombre} - "
                f"{cita.servicio.nombre}"
                f"</p>"
            )

    if cantidad == 0:
        return HttpResponse(
            "<h1>Citas pendientes</h1>"
            "<p>No existen citas pendientes.</p>"
        )

    respuesta += f"<p>Total pendientes: {cantidad}</p>"

    return HttpResponse(respuesta)

def servicios_economicos(request):

    umbral = 15000

    servicios = Servicio.objects.all()

    respuesta = (
        f"<h1>Servicios económicos</h1>"
        f"<p>Servicios bajo ${umbral}</p>"
    )

    for servicio in servicios:

        if servicio.precio < umbral:

            respuesta += (
                f"<p>"
                f"{servicio.nombre} - "
                f"${servicio.precio}"
                f"</p>"
            )

    return HttpResponse(respuesta)

def estado_cita(request, numero):

    try:
        cita = Cita.objects.get(id=numero)
    except Cita.DoesNotExist:
        return HttpResponse("La cita no existe.")

    if cita.estado == "pendiente":
        mensaje = "La cita está pendiente de confirmación."

    elif cita.estado == "confirmada":
        mensaje = "La cita está confirmada."

    elif cita.estado == "atendida":
        mensaje = "La cita ya fue atendida."

    else:
        mensaje = "Estado desconocido."

    return HttpResponse(
        f"<h1>Estado de la cita</h1>"
        f"<p>{mensaje}</p>"
    )

def detalle_cita(request, numero):

    try:
        cita = Cita.objects.get(id=numero)
    except Cita.DoesNotExist:
        return HttpResponse(
            "<h1>Error</h1>"
            "<p>La cita indicada no existe.</p>"
        )

    pagos = cita.pagos.all()

    total_pagado = 0

    respuesta = (
        f"<h1>Detalle de cita</h1>"
        f"<p>Cliente: {cita.cliente.nombre}</p>"
        f"<p>Servicio: {cita.servicio.nombre}</p>"
        f"<p>Precio: ${cita.servicio.precio}</p>"
        f"<p>Estado: {cita.estado}</p>"
        f"<h2>Pagos</h2>"
    )

    for pago in pagos:

        total_pagado += pago.monto

        respuesta += (
            f"<p>"
            f"${pago.monto} - "
            f"{pago.metodo_pago}"
            f"</p>"
        )

    saldo = cita.servicio.precio - total_pagado

    respuesta += f"<p>Total pagado: ${total_pagado}</p>"

    if saldo <= 0:
        respuesta += "<p>La cita está completamente saldada.</p>"
    else:
        respuesta += f"<p>Saldo pendiente: ${saldo}</p>"

    return HttpResponse(respuesta)

def duracion_citas(request):

    citas = Cita.objects.all()

    total_minutos = 0

    for cita in citas:

        if cita.estado == "confirmada":
            total_minutos += cita.servicio.duracion_min

    horas = total_minutos // 60
    minutos = total_minutos % 60

    return HttpResponse(
        f"<h1>Tiempo agendado</h1>"
        f"<p>Total: {total_minutos} minutos</p>"
        f"<p>{horas} horas y {minutos} minutos</p>"
    )

def citas_por_cliente(request):

    clientes = Cliente.objects.all()

    respuesta = "<h1>Citas por cliente</h1>"

    for cliente in clientes:

        cantidad = 0

        for cita in cliente.citas.all():
            cantidad += 1

        if cantidad > 1:
            marca = "*"
        else:
            marca = ""

        respuesta += (
            f"<p>"
            f"{cliente.nombre}: {cantidad} citas {marca}"
            f"</p>"
        )

    return HttpResponse(respuesta)

def informe_general(request):

    citas = Cita.objects.all()

    total_citas = 0

    pendientes = 0
    confirmadas = 0
    atendidas = 0

    total_pagado = 0
    total_pendiente = 0

    for cita in citas:

        total_citas += 1

        if cita.estado == "pendiente":
            pendientes += 1

        elif cita.estado == "confirmada":
            confirmadas += 1

        elif cita.estado == "atendida":
            atendidas += 1

        pagado_cita = 0

        for pago in cita.pagos.all():
            pagado_cita += pago.monto
            total_pagado += pago.monto

        pendiente_cita = cita.servicio.precio - pagado_cita

        if pendiente_cita > 0:
            total_pendiente += pendiente_cita

    return HttpResponse(
        f"<h1>Informe general</h1>"
        f"<p>Total de citas: {total_citas}</p>"
        f"<p>Pendientes: {pendientes}</p>"
        f"<p>Confirmadas: {confirmadas}</p>"
        f"<p>Atendidas: {atendidas}</p>"
        f"<p>Total pagado: ${total_pagado}</p>"
        f"<p>Pendiente de cobro: ${total_pendiente}</p>"
    )

def servicios_populares(request):

    servicios = Servicio.objects.all()
    citas = Cita.objects.all()

    mayor_cantidad = 0
    servicio_mas_pedido = None

    respuesta = "<h1>Servicios más solicitados</h1>"

    for servicio in servicios:

        cantidad = 0

        for cita in citas:

            if cita.servicio.id == servicio.id:
                cantidad += 1

        respuesta += (
            f"<p>"
            f"{servicio.nombre}: {cantidad} citas"
            f"</p>"
        )

        if cantidad > mayor_cantidad:
            mayor_cantidad = cantidad
            servicio_mas_pedido = servicio

    if servicio_mas_pedido is not None:

        respuesta += (
            f"<h2>Servicio más pedido</h2>"
            f"<p>"
            f"{servicio_mas_pedido.nombre} "
            f"con {mayor_cantidad} citas"
            f"</p>"
        )

    return HttpResponse(respuesta)