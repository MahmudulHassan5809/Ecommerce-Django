# Generated by Django 3.0.7 on 2020-10-16 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_transactionmethod'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_option',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_option_order', to='cart.TransactionMethod'),
        ),
    ]
