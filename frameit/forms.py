from django import forms
from .models import Customer, Material, Job, MatWindow, JobComponent, Invoice

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone']

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'type', 'code', 'price', 'width', 'bay_number']

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['customer', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].queryset = Customer.objects.all()

class MatWindowForm(forms.ModelForm):
    class Meta:
        model = MatWindow
        fields = ['width', 'height', 'x_position', 'y_position']

class JobComponentForm(forms.ModelForm):
    class Meta:
        model = JobComponent
        fields = ['material', 'quantity', 'type', 'order']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['material'].queryset = Material.objects.all()

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['customer', 'jobs', 'amount_paid']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].queryset = Customer.objects.all()
        self.fields['jobs'].queryset = Job.objects.all()

class JobCalculationForm(forms.Form):
    job_id = forms.IntegerField()
    # Add any additional fields needed for calculations

class WorkOrderForm(forms.Form):
    job_id = forms.IntegerField()
    # Add any additional fields needed for work order generation
