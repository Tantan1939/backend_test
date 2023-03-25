from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=200)),
                ('brand_code', models.CharField(max_length=100)),
                ('logo', models.ImageField(upload_to='brand/logos')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_number', models.TextField(default='customernum',
                 editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('Status', models.CharField(choices=[
                 ('A', 'Active'), ('T', 'Terminated')], max_length=1)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT,
                 related_name='customer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_added'],
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('invoice_number', models.TextField(default='invoicenum',
                 editable=False, primary_key=True, serialize=False)),
                ('description', models.TextField(null=True)),
                ('total_price', models.DecimalField(
                    decimal_places=2, max_digits=10, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT,
                 related_name='customer_invoice', to='shop.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_number', models.TextField(default='productnum',
                 editable=False, primary_key=True, serialize=False)),
                ('currency', models.CharField(choices=[
                 ('USD', 'US Dollars'), ('PHP', 'Philippine Peso')], max_length=3)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('next_billing_date', models.DateField()),
                ('previous_billing_date', models.DateField()),
                ('Status', models.CharField(choices=[
                 ('A', 'Active'), ('T', 'Terminated')], max_length=1)),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT,
                 related_name='add_product_by', to=settings.AUTH_USER_MODEL)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT,
                 related_name='product', to='shop.brand')),
                ('customer', models.ManyToManyField(
                    related_name='customer_items', through='shop.Invoice', to='shop.customer')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT,
                 related_name='update_product_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='invoice',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT,
                                    related_name='product_invoice', to='shop.product'),
        ),
        migrations.CreateModel(
            name='customers_brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT,
                 related_name='customer', to='shop.brand')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT,
                 related_name='customer_brand', to='shop.customer')),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='brand',
            field=models.ManyToManyField(
                related_name='brand_customer', through='shop.customers_brand', to='shop.brand'),
        ),
        migrations.AddField(
            model_name='customer',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT,
                                    related_name='update_customer', to=settings.AUTH_USER_MODEL),
        ),
    ]
