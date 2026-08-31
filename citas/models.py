from django.db import models


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.nombre


class Servicio(models.Model):
    nombre = models.CharField(max_length=80)
    precio = models.IntegerField()
    duracion_min = models.IntegerField(default=30)

    def __str__(self):
        return self.nombre


class Cita(models.Model):

    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("confirmada", "Confirmada"),
        ("atendida", "Atendida"),
    ]

    # PROTECT evita borrar un cliente si todavía tiene citas asociadas.
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name="citas"
    )

    # PROTECT evita borrar un servicio que esté siendo utilizado en una cita.
    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.PROTECT,
        related_name="citas"
    )

    fecha_hora = models.DateTimeField()

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="pendiente"
    )

    def __str__(self):
        return f"Cita {self.id} - {self.cliente.nombre}"


class Pago(models.Model):

    cita = models.ForeignKey(
        Cita,
        on_delete=models.CASCADE,
        related_name="pagos"
    )

    monto = models.IntegerField()

    metodo_pago = models.CharField(max_length=50)

    def __str__(self):
        return f"Pago {self.id} - ${self.monto}"