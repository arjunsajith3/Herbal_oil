from django.db import models
from my_admin.models import Product
from django.utils import timezone
from decimal import Decimal


class Bookingdetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    oilSize = models.CharField(max_length=20)
    unitPrice = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()


    total_qty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    booked_at = models.DateTimeField(default=timezone.now)

    payment_status = models.CharField(
        max_length=20,
        default="Pending",
        choices=[
            ("Pending", "Pending"),
            ("Paid", "Paid"),
            ("Failed", "Failed"),
        ]
    )

    order_status = models.CharField(
        max_length=20,
        default="Pending",
        choices=[
            ("Pending", "Pending"),
            ("Processing", "Processing"),
            ("Shipped", "Shipped"),
            ("Delivered", "Delivered"),
            ("Cancelled", "Cancelled"),
        ]
    )

    payment_method = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        choices=[
            ("Card", "Card"),
            ("UPI", "UPI"),
            ("NetBanking", "NetBanking"),
            ("COD", "Cash on Delivery"),
            ("Wallet", "Wallet"),
        ]
    )

    note = models.TextField(null=True, blank=True)

    custName = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    alt_phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.total_amount = Decimal(self.unitPrice) * int(self.quantity)
        self.total_qty = self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        if self.product:
            return f"{self.product.product_name} - {self.custName}"
        return f"{self.custName}"

