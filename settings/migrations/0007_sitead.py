# Generated by Django 3.0.7 on 2020-10-24 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0006_aboutus'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteAd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('link', models.URLField()),
                ('image', models.ImageField(upload_to='site_ad')),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Site Ad',
                'verbose_name_plural': '4.Site Ad',
            },
        ),
    ]