# Generated by Django 5.0.9 on 2024-12-03 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='estado',
            name='codigo_uf_importacao',
            field=models.IntegerField(blank=True, null=True, verbose_name='CodigoImportacao'),
        ),
    ]