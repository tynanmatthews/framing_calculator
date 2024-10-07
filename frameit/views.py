from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import get_template
from django.views import View
from django.utils import timezone
from django.db.models import Sum, Q
from django.core.paginator import Paginator

from .models import *
from .forms import JobComponentForm, JobForm, InvoiceForm, MatWindowForm, MaterialForm, InvoiceEmailForm

# From Claude's email code, check this thoroughly
from django.urls import reverse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import io
from datetime import datetime
from django.template.loader import get_template
# from xhtml2pdf import pisa for email sending, stub for now

class HomeView(View):
    def get(self, request):
        return render(request, 'base.html')

class JobCreationView(View):
    def get(self, request):
        job_form = JobForm()
        mat_window_form = MatWindowForm()
        job_component_form = JobComponentForm()
        frame_materials = Material.objects.filter(type='frame')
        mat_materials = Material.objects.filter(type='mat')
        glass_materials = Material.objects.filter(type='glass')

        context = {
            'job_form': job_form,
            'job_component_form': job_component_form,
            'mat_window_form': mat_window_form,
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

            return redirect('frameit:job_detail', job_id=job.id)

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
            return redirect(reverse('frameit:material_list'))
        return render(request, 'material_create.html', {'form':form})


class MaterialEditView(View):
    def get(self, request, material_id):
        material = get_object_or_404(Material, id=material_id)
        form = MaterialForm(instance=material)
        context = {
            'material': material,
            'form': form,
        }
        return render(request, 'material_edit.html', context)

    def post(self, request, material_id):
        material = get_object_or_404(Material, id=material_id)
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            material = form.save()
            return redirect(reverse('frameit:material_list'))
        context = {
            'form': form,
            'material': material,
        }
        return render(request, 'material_edit.html', context)

class InvoiceCreationView(View):
        def get(self, request):
            form = InvoiceForm()
            # Annotate jobs with their total price
            return render(request, 'invoice_creation.html', {'form': form})

        def post(self, request):
            form = InvoiceForm(request.POST)
            if form.is_valid():
                invoice = form.save()
                return redirect(reverse('frameit:invoice_detail', kwargs={'invoice_id': invoice.id}))

            # If form is invalid, re-render with errors
            jobs = Job.objects.annotate(total_price=Sum('jobcomponent__price'))
            form.fields['jobs'].queryset = jobs
            form.fields['jobs'].widget.attrs['data-price'] = {job.id: str(job.total_price) for job in jobs}
            return render(request, 'invoice_creation.html', {'form': form})

class InvoiceDetailView(View):
    def get(self, request, invoice_id):
        invoice = get_object_or_404(Invoice, id=invoice_id)
        return render(request, 'invoice_detail.html', {'invoice': invoice})

class InvoiceEditView(View):
    def get(self, request, invoice_id):
        invoice = get_object_or_404(Invoice, id=invoice_id)
        form = InvoiceForm(instance=invoice)

        # Annotate jobs with their total price
        jobs = Job.objects.annotate(total_price=Sum('jobcomponent__price'))
        form.fields['jobs'].queryset = jobs
        form.fields['jobs'].widget.attrs['data-price'] = {job.id: str(job.total_price) for job in jobs}

        context = {
            'form': form,
            'invoice': invoice,
        }
        return render(request, 'invoice_edit.html', context)

    def post(self, request, invoice_id):
        invoice = get_object_or_404(Invoice, id=invoice_id)
        form = InvoiceForm(request.POST, instance=invoice)

        if form.is_valid():
            updated_invoice = form.save()

            # Recalculate total amount based on selected jobs
            total_amount = sum(job.total_price for job in updated_invoice.jobs.all())
            updated_invoice.total_amount = total_amount
            updated_invoice.save()

            return redirect(reverse('frameit:invoice_detail', kwargs={'invoice_id': invoice.id}))

        # If form is invalid, re-render with errors
        jobs = Job.objects.annotate(total_price=Sum('jobcomponent__price'))
        form.fields['jobs'].queryset = jobs
        form.fields['jobs'].widget.attrs['data-price'] = {job.id: str(job.total_price) for job in jobs}

        context = {
            'form': form,
            'invoice': invoice,
        }
        return render(request, 'invoice_edit.html', context)

class InvoiceListView(View):
    def get(self, request):
        invoices = Invoice.objects.all().order_by('-date_created')

        # Filter by customer name
        customer_filter = request.GET.get('customer')
        if customer_filter:
            invoices = invoices.filter(customer__name__icontains=customer_filter)

        # Filter by date range
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            invoices = invoices.filter(date_created__date__range=[start_date, end_date])

        # Pagination
        paginator = Paginator(invoices, 20)  # Show 20 invoices per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'invoices': page_obj,
        }
        return render(request, 'invoice_list.html', context)

class InvoicePrintView(LoginRequiredMixin, View):
    def get(self, request, invoice_id):
        invoice = get_object_or_404(Invoice, id=invoice_id)

        # Calculate the due date (e.g., 30 days from creation)
        due_date = invoice.date_created + timedelta(days=30)

        context = {
            'invoice': invoice,
            'due_date': due_date,
        }
        return render(request, 'invoice_print.html', context)

class InvoiceEmailView(LoginRequiredMixin, View):
    def get(self, request, invoice_id):
        invoice = get_object_or_404(Invoice, id=invoice_id)
        initial_data = {
            'to_email': invoice.customer.email,
            'subject': f'Invoice #{invoice.id} from Your Company',
            'message': f'Dear {invoice.customer.name},\n\nPlease find attached the invoice #{invoice.id} for your recent order. The total amount due is ${invoice.balance_due:.2f}.\n\nThank you for your business.\n\nBest regards,\nYour Company'
        }
        form = InvoiceEmailForm(initial=initial_data)
        return render(request, 'invoice_email.html', {'form': form, 'invoice': invoice})

    def post(self, request, invoice_id):
        invoice = get_object_or_404(Invoice, id=invoice_id)
        form = InvoiceEmailForm(request.POST)
        if form.is_valid():
            to_email = form.cleaned_data['to_email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            attach_pdf = form.cleaned_data['attach_pdf']

            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[to_email],
            )

            if attach_pdf:
                pdf = self.generate_pdf(invoice)
                email.attach(f'invoice_{invoice.id}.pdf', pdf, 'application/pdf')

            email.send()

            messages.success(request, f'Invoice #{invoice.id} has been emailed to {to_email}')
            return redirect(reverse('frameit:invoice_detail', kwargs={'invoice_id': invoice.id}))

        return render(request, 'invoice_email.html', {'form': form, 'invoice': invoice})

    def generate_pdf(self, invoice):
        template = get_template('invoice_print.html')
        html = template.render({'invoice': invoice})
        result = io.BytesIO()
        # pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
        print("PDF rendering isn't implemented yet")
        return None
        if not pdf.err:
            return result.getvalue()
        return None

class JobCalculationView(View):
    def post(self, request):
        # This view will handle the AJAX requests for real-time price calculations
        # You'll need to implement the calculation logic here
        pass

class WorkOrderGenerationView(View):
    def get(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)
        context = {
            "job": job,
            'current_date': timezone.now(),
        }
        # Generate work order logic here
        return render(request, 'work_order.html', context)
