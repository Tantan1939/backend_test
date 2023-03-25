from shop.models import *
from django.db.models import Prefetch
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


def display_data(datas):
    for key, data in enumerate(datas):
        print(f"{key}: {data}")


def get_due_products():
    return display_data(Product.get_due_products.all())


def create_new_invoice():
    products = Product.get_due_products.prefetch_related(Prefetch(
        'customer', queryset=Customer.objects.filter(Status='A'), to_attr="customers"))

    if products:
        list_of_invoices = []
        next_date = (datetime.today() + relativedelta(days=30)
                     ).strftime("%Y-%m-%d")
        make_next_billing_date = datetime.strptime(next_date, "%Y-%m-%d")

        for product in products:
            for customer in product.customers:
                new_invoice = Invoice.objects.create(
                    customer=customer, description="New invoice", product=product, total_price=100)
                list_of_invoices.append(new_invoice)

            product.previous_billing_date = date.today()
            product.next_billing_date = make_next_billing_date
            product.save()
        else:
            return display_data(list_of_invoices)

    return "No due products"
