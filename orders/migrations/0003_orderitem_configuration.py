# Generated by Django 5.1.1 on 2024-10-08 07:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configurate', '0006_rename_quantity_productconfiguration_quantity_available'),
        ('orders', '0002_alter_order_options_alter_orderitem_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='configuration',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='configurate.productconfiguration'),
        ),
    ]
