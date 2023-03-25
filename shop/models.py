from django.db import models, transaction
from datetime import date
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db.models import Count, F, Q


class Brand(models.Model):
    brand_name = models.CharField(max_length=200)
    brand_code = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='brand/logos')


class Customer(models.Model):
    class status_choices(models.TextChoices):
        is_active = 'A', _('Active')
        is_terminated = 'T', _('Terminated')

    customer_number = models.TextField(
        primary_key=True, editable=False, default='customernum')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    brand = models.ManyToManyField(
        Brand, related_name="brand_customer", through='customers_brand')
    added_by = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name="customer", null=True, blank=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name="update_customer", null=True, blank=True)
    Status = models.CharField(max_length=1, choices=status_choices.choices)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer_number

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def status(self):
        return self.get_Status_display()

    @classmethod
    def change_status(cls, customerNumber, change):
        with transaction.atomic():
            get_customer_instance = cls.objects.select_for_update().get(
                customer_number=customerNumber)
            get_customer_instance.Status = change
            get_customer_instance.save()

    class Meta:
        ordering = ['-date_added']


class customers_brand(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.RESTRICT, related_name='customer_brand')
    brand = models.ForeignKey(
        Brand, on_delete=models.RESTRICT, related_name='customer')


class due_products(models.Manager):
    def get_queryset(self):
        return super().get_queryset().alias(due_customers=Count('customer', filter=Q(customer__Status='A'))).filter(next_billing_date__lte=date.today(), due_customers__gte=1)


class Product(models.Model):
    class status_choices(models.TextChoices):
        is_active = 'A', _('Active')
        is_terminated = 'T', _('Terminated')

    class currency_choices(models.TextChoices):
        us_dollar = 'USD', _('US Dollars')
        peso = 'PHP', _('Philippine Peso')

    product_number = models.TextField(
        primary_key=True, editable=False, default='productnum')
    currency = models.CharField(max_length=3, choices=currency_choices.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    customer = models.ManyToManyField(
        Customer, through='Invoice', related_name='customer_items')
    description = models.TextField()
    brand = models.ForeignKey(
        Brand, on_delete=models.RESTRICT, related_name='product')
    next_billing_date = models.DateField()
    previous_billing_date = models.DateField()
    Status = models.CharField(max_length=1, choices=status_choices.choices)
    added_by = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name="add_product_by", null=True, blank=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name="update_product_by", null=True, blank=True)

    objects = models.Manager()
    get_due_products = due_products()

    def __str__(self):
        return self.product_number

    @classmethod
    def change_status(cls, productNumber, change):
        with transaction.atomic():
            get_product_instance = cls.objects.select_for_update().get(
                product_number=productNumber)
            get_product_instance.Status = change
            get_product_instance.save()

    def status(self):
        return self.get_Status_display()


class Invoice(models.Model):
    invoice_number = models.TextField(
        primary_key=True, editable=False, default='invoicenum')
    customer = models.ForeignKey(
        Customer, on_delete=models.RESTRICT, related_name='customer_invoice')
    description = models.TextField(null=True)
    product = models.ForeignKey(
        Product, on_delete=models.RESTRICT, related_name='product_invoice')
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return self.invoice_number
