from django.db import models

# Create your models here.
class Customer(models.Model):
    """
    Customers place orders for frames.

    Attributes:
        name - Name of the customer, searchable
        phone_number
        email_address
    """
    name = models.CharField(max_length=200)
    phone_number = models.IntegerField()
    email_address = models.CharField(max_length=200)

class Order(models.Model):
    """
    An order is placed by a customer, it contains one or more jobs.

    Attributes
        customer
        date_submitted - What day was the order created?
        date_completed - What day was the order completed?
        date_contacted - What day was the customer last contacted?
        status - "New" | "In Progress" | "Awaiting Stock" | "Customer Contacted" | "Delivery Scheduled" | "Completed"
        jobs_context - List of Jobs assigned to this Order
        comments - any details about the job not otherwise capture


    Methods
        (?) check_status
    """
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class Frame(models.Model):
    """
    Customer will order a frame to be assembled.

    Frames are a complex datatype and will be stored
    in the frames app in the future
    params:
        moulding
        width
        height
        face_width
        face_height
        content
        inset
        padding_left
        padding_right
        padding_top
        padding_bottom
    """

class Job(models.Model):
    """
    A job is something to be completed within the factory, each job has one frame.

    Attributes:
        order - Which order does this job belong to?
        frame - A frame specification
        status - How is the job progressing? "New" | "In Progress" | "Awaiting stock" | "Completed"
        bay - Which bay can the frame be found it?
        completed - boolean
            completed_by - Staff member
            date_completed
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    frame = models.OneToOneField(Frame, on_delete=models.CASCADE)
