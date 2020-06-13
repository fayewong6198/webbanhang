from django.db import models

from datetime import datetime

from accounts.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name


class Product(models.Model):
    sku = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/')

    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="users")

    def get_total(self):
        price = 0
        for product in self.products.all():
            price = price + product.product.price * product.quantity

        return price

    total = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateField(default=datetime.now)


class ProductInCart(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    created_at = models.DateField(default=datetime.now)


class Delivery(models.Model):
    name = models.CharField(max_length=255)

    created_at = models.DateField(default=datetime.now)

    def __str__(self):
        return self.name


class PaymentType(models.Model):
    name = models.CharField(max_length=255)

    created_at = models.DateField(default=datetime.now)

    def __str__(self):
        return self.name


class Payment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user')
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    address = models.TextField()
    paymentType = models.ForeignKey(
        PaymentType, on_delete=models.CASCADE, related_name='payments')
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)

    total = models.DecimalField(max_digits=20, decimal_places=2)

    created_at = models.DateField(default=datetime.now)

    def __str__(self):
        return self.name


class ProductInPayment(models.Model):
    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=2)

    created_at = models.DateField(default=datetime.now)
