# Generated by Django 3.0.7 on 2020-09-26 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('slug', models.CharField(max_length=150)),
                ('image', models.ImageField(upload_to='blog')),
                ('description', models.TextField()),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_posts', to='blog.Category')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': '2.Posts',
            },
        ),
    ]