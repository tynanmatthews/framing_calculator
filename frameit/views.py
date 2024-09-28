from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse
# Create your views here.
def index(request):
    return HttpResponse("Hello lil fella!, welcome to the frameit index!")

# Views

from django.views import View
from .models import *
from .forms import JobForm, InvoiceForm, MaterialForm

class JobCreationView(View):
    def get(self, request):
        form = JobForm()
        frame_materials = Material.objects.filter(type='frame')
        mat_materials = Material.objects.filter(type='mat')
        glass_materials = Material.objects.filter(type='glass')

        context = {
            'form': form,
            'frame_materials': frame_materials,
            'mat_materials': mat_materials,
            'glass_materials': glass_materials,
        }
        return render(request, 'job_creation.html', context)

    def post(self, request):
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.total_price = 0  # You'll need to calculate this
            job.save()

            # Process job components (frames, mats, glass)
            # Create MatWindow
            # Update job total price

            return redirect('job_detail', job_id=job.id)

        # If form is not valid, re-render the page with error messages
        frame_materials = Material.objects.filter(type='frame')
        mat_materials = Material.objects.filter(type='mat')
        glass_materials = Material.objects.filter(type='glass')

        context = {
            'form': form,
            'frame_materials': frame_materials,
            'mat_materials': mat_materials,
            'glass_materials': glass_materials,
        }
        return render(request, 'job_creation.html', context)

class JobDetailView(View):
    def get(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)
        context = {
            'job': job,
        }
        return render(request, 'job_detail.html', context)

class MaterialListView(View):
    def get(self, request):
        materials = Material.objects.all().order_by('type', 'name')
        context = {
            'materials': materials,
        }
        return render(request, 'material_list.html', context)

class MaterialCreateView(View):
    def get(self, request):
        form = MaterialForm()
        return render(request, 'material_create.html', {'form': form})

    def post(self, request):
        form = MaterialForm(request.POST)
        if form.is_valid():
            material = form.save()
            return redirect(reverse('material_list'))
        return render(request, 'material_create.html', {'form':form})


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
