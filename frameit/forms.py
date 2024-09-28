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
        widgets = {
            'type': forms.Select(choices=[
                ('frame', 'Frame'),
                ('mat', 'Mat'),
                ('glass', 'Glass'),
            ]),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['width'].required = False
        self.fields['bay_number'].required = False

    def clean(self):
        cleaned_data = super().clean()
        material_type = cleaned_data.get('type')
        width = cleaned_data.get('width')
        bay_number = cleaned_data.get('bay_number')

        if material_type == 'frame':
            if not width:
                self.add_error('width', 'Width is required for frames.')
            if not bay_number:
                self.add_error('bay_number', 'Bay number is required for frames.')
        else:
            cleaned_data['width'] = None
            cleaned_data['bay_number'] = None

        return cleaned_data


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
