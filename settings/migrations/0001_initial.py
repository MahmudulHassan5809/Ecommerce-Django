# Generated by Django 3.0.7 on 2020-10-24 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=255)),
                ('site_phone', models.CharField(max_length=20)),
                ('site_email', models.EmailField(max_length=254)),
                ('site_address', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'SiteInfo',
                'verbose_name_plural': '1.SiteInfo',
            },
        ),
    ]