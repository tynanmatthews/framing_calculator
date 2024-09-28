from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    return HttpResponse("Hello lil fella!, welcome to the frameit index!")

# Views

from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .forms import JobForm, InvoiceForm  # You'll need to create these forms

class JobCreationView(View):
    def get(self, request):
        form = JobForm()
        return render(request, 'job_creation.html', {'form': form})

    def post(self, request):
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save()
            return redirect('job_detail', job_id=job.id)
        return render(request, 'job_creation.html', {'form': form})

class JobDetailView(View):
    def get(self, request, job_id):
        job = Job.objects.get(id=job_id)
        return render(request, 'job_detail.html', {'job': job})

class MaterialListView(View):
    def get(self, request):
        materials = Material.objects.all()
        return render(request, 'material_list.html', {'materials': materials})

class InvoiceCreationView(View):
    def get(self, request):
        form = InvoiceForm()
        return render(request, 'invoice_creation.html', {'form': form})

    def post(self, request):
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save()
            return redirect('invoice_detail', invoice_id=invoice.id)
        return render(request, 'invoice_creation.html', {'form': form})

class InvoiceDetailView(View):
    def get(self, request, invoice_id):
        invoice = Invoice.objects.get(id=invoice_id)
        return render(request, 'invoice_detail.html', {'invoice': invoice})

class JobCalculationView(View):
    def post(self, request):
        # This view will handle the AJAX requests for real-time price calculations
        # You'll need to implement the calculation logic here
        pass

class WorkOrderGenerationView(View):
    def get(self, request, job_id):
        job = Job.objects.get(id=job_id)
        # Generate work order logic here
        return render(request, 'work_order.html', {'job': job})
