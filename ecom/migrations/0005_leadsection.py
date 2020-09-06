# Generated by Django 3.0.7 on 2020-09-05 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0004_product_discount'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeadSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_lead', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='category_first_lead', to='ecom.Category')),
                ('second_lead', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='category_second_lead', to='ecom.Category')),
                ('third_lead', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='category_third_lead', to='ecom.Category')),
            ],
            options={
                'verbose_name_plural': '3.Lead Sections',
            },
        ),
    ]