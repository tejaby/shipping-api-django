from django.db import models

from locations.models import Location


class Shipment(models.Model):
    order_number = models.CharField(max_length=20)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    department = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="shipments")
    recipient = models.CharField(max_length=100)
    store = models.CharField(max_length=200)

    def __str__(self):
        return f"Shipment {self.order_number} - {self.weight}kg to {self.address} (Status: {self.status})"
