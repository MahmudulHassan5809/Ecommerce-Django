# Generated by Django 3.0.7 on 2020-10-24 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteinfo',
            name='logo',
            field=models.ImageField(default='logo.png', upload_to='settings'),
            preserve_default=False,
        ),
    ]