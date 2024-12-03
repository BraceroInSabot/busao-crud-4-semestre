# Generated by Django 5.0.9 on 2024-12-01 16:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Cidade')),
            ],
            options={
                'db_table': 'Cidade',
            },
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Estado')),
                ('sigla', models.CharField(max_length=2, verbose_name='Sigla')),
            ],
            options={
                'db_table': 'Estado',
            },
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rua', models.CharField(max_length=255, verbose_name='Rua')),
                ('bairro', models.CharField(max_length=255, verbose_name='Bairro')),
                ('numero', models.CharField(max_length=10, verbose_name='Número')),
                ('cep', models.CharField(max_length=10, verbose_name='CEP')),
                ('complemento', models.CharField(blank=True, max_length=255, null=True, verbose_name='Complemento')),
                ('cidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enderecos', to='application.cidade')),
            ],
            options={
                'db_table': 'Endereco',
            },
        ),
        migrations.AddField(
            model_name='cidade',
            name='estado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cidades', to='application.estado'),
        ),
    ]
