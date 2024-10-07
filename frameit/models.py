from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Material(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)  # e.g., 'mat', 'frame', 'glass'
    code = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    width = models.IntegerField(null=True, blank=True)  # for frames
    bay_number = models.IntegerField(null=True, blank=True)  # for frames

    def __str__(self):
        return self.name + " " + self.type

class Job(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    special_instructions = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.description

    @property
    def total_price(self):
        return self.jobcomponent_set.aggregate(total=Sum('price'))['total'] or 0

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
    TYPE_CHOICES = (
        ('frame', 'Frame'),
        ('mat', 'Mat'),
        ('glass', 'Glass'),
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)  # e.g., 'mat', 'frame', 'glass'
    order = models.IntegerField(default=0)  # for multiple mats/frames

    def get_type_display(self):
        return dict(self.TYPE_CHOICES)[self.type]

    def __str__(self):
        return self.material + " " + self.type

class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    jobs = models.ManyToManyField(Job)

    @property
    def balance_due(self):
        return self.total_amount - self.amount_paid

    @property
    def total_amount(self):
        return self.jobs_set.aggregate(total=Sum('total_price'))['total'] or 0

    def __str__(self):
        return self.customer.name + " " + jobs.description
