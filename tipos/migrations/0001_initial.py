# Generated by Django 5.1.2 on 2024-11-14 21:21

import django.db.models.deletion
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_do_evento', models.CharField(choices=[('CON', 'Conferencia'), ('PLA', 'Palestra'), ('WKS', 'Workshop'), ('SAL', 'Sala'), ('TER', 'Terreno')], default='CAS', max_length=3)),
                ('identificador', models.CharField(max_length=10, unique=True)),
                ('data_inicio', models.CharField(max_length=10)),
                ('hora_inicio', models.CharField(max_length=10)),
                ('data_final', models.CharField(max_length=10)),
                ('hora_final', models.CharField(max_length=10)),
                ('cep', models.CharField(max_length=10)),
                ('endereco', models.CharField(max_length=255)),
                ('bairro', models.CharField(max_length=100)),
                ('cidade', models.CharField(max_length=100)),
                ('estado', models.CharField(max_length=2)),
                ('email_contato', models.EmailField(max_length=50)),
                ('valor_inscricao', models.DecimalField(decimal_places=2, max_digits=8)),
                ('descricao', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Participante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('cpf', models.CharField(max_length=100)),
                ('telefone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='ImagemEvento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', models.ImageField(upload_to='eventos/')),
                ('destaque', models.BooleanField(default=False)),
                ('data_upload', models.DateTimeField(auto_now_add=True)),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagens', to='eventos.evento')),
            ],
        ),
        migrations.CreateModel(
            name='Inscricao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_pagamento', models.DateField()),
                ('valor_insrcicao', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pago', models.BooleanField(default=False)),
                ('material', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0.0'), max_digits=8, null=True)),
                ('almoco', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0.0'), max_digits=8, null=True)),
                ('certificado', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0.0'), max_digits=8, null=True)),
                ('outras_taxas', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0.0'), max_digits=8, null=True)),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventos.evento')),
                ('participante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventos.participante')),
            ],
        ),
    ]