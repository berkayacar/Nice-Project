# Generated by Django 5.2 on 2025-04-29 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'contact',
            },
        ),
        migrations.CreateModel(
            name='KullaniciBilgileri',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isim', models.CharField(max_length=100)),
                ('soyisim', models.CharField(max_length=100)),
                ('program', models.CharField(max_length=100)),
                ('telefon', models.CharField(max_length=15)),
                ('kredi_karti_numarasi', models.CharField(max_length=16)),
                ('son_kullanma_tarihi', models.CharField(max_length=5)),
                ('cvv', models.CharField(default='000', max_length=3)),
            ],
        ),
    ]
