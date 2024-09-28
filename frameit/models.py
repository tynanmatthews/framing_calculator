from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

class Material(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)  # e.g., 'mat', 'frame', 'glass'
    code = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    width = models.IntegerField(null=True, blank=True)  # for frames
    bay_number = models.IntegerField(null=True, blank=True)  # for frames

class Job(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

class MatWindow(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    width = models.IntegerField()
    height = models.IntegerField()
    x_position = models.IntegerField()
    y_position = models.IntegerField()

class JobComponent(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=50)  # e.g., 'mat', 'frame', 'glass'
    order = models.IntegerField(default=0)  # for multiple mats/frames

class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    jobs = models.ManyToManyField(Job)
