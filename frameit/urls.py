from django.urls import path
from . import views

app_name = 'frameit'

urlpatterns = [
    path('', views.index, name='index'),
    path('job/create/', views.JobCreationView.as_view(), name='job_create'),
    path('job/<int:job_id>/', views.JobDetailView.as_view(), name='job_detail'),
    path('materials/', views.MaterialListView.as_view(), name='material_list'),
    path("materials/create/", views.MaterialCreateView.as_view(), name='material_create'),
    path("materials/<int:material_id/edit/", views.MaterialEditView.as_view(), name='material_edit'),
    path('invoice/create/', views.InvoiceCreationView.as_view(), name='invoice_create'),
    path('invoice/<int:invoice_id>/', views.InvoiceDetailView.as_view(), name='invoice_detail'),
    path('job/calculate/', views.JobCalculationView.as_view(), name='job_calculate'),
    path('job/<int:job_id>/work-order/', views.WorkOrderGenerationView.as_view(), name='work_order_generate'),
]
