# Generated by Django 3.2.12 on 2022-04-06 19:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=60, unique=True)),
                ('uf', models.CharField(max_length=2, unique=True)),
            ],
            options={
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Fiscal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=150, verbose_name='Nome do Fiscal')),
                ('crea', models.CharField(max_length=150, verbose_name='CREA')),
                ('matricula', models.CharField(max_length=150, verbose_name='Matrícula')),
                ('dt_inclusao', models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')),
            ],
        ),
        migrations.CreateModel(
            name='Nota_Fiscal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('n_nota', models.IntegerField(verbose_name='N. da nota')),
                ('data', models.DateField(verbose_name='Data de expedição')),
                ('valor', models.CharField(max_length=20, verbose_name='Valor da nota')),
                ('periodo', models.CharField(max_length=5, verbose_name='Período')),
                ('url', models.CharField(max_length=300, verbose_name='Link da nota')),
                ('dt_inclusao', models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')),
            ],
        ),
        migrations.CreateModel(
            name='Obra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('objeto_da_obra', models.CharField(max_length=150, verbose_name='Objeto da obra')),
                ('populacao_atendida', models.CharField(max_length=150, verbose_name='População atendida')),
                ('valor_previsto', models.IntegerField(verbose_name='Valor previsto')),
                ('justificativa', models.TextField(verbose_name='Justificativa')),
                ('dt_inclusao', models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')),
                ('cadastrado_por', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Obra_Fiscal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('r', 'Responsável'), ('s', 'Suplente'), ('f', 'Férias')], max_length=1)),
                ('fiscal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fiscalizacao.fiscal')),
                ('obra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fiscalizacao.obra')),
            ],
        ),
        migrations.AddField(
            model_name='obra',
            name='fiscal',
            field=models.ManyToManyField(through='fiscalizacao.Obra_Fiscal', to='fiscalizacao.Fiscal'),
        ),
        migrations.AddField(
            model_name='obra',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='fiscalizacao.status', verbose_name='Situação'),
        ),
        migrations.CreateModel(
            name='Fotos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=300)),
                ('obra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fiscalizacao.obra')),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=150, verbose_name='Nome da empresa')),
                ('cnpj', models.CharField(max_length=14, verbose_name='CNPJ')),
                ('dt_inclusao', models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')),
                ('cadastrado_por', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Contrato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt_inclusao', models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='fiscalizacao.empresa', verbose_name='Empresa contratada')),
                ('nota_fiscal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='fiscalizacao.nota_fiscal')),
                ('obra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fiscalizacao.obra')),
            ],
        ),
        migrations.CreateModel(
            name='Aditivos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contrato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fiscalizacao.contrato')),
                ('nota_fiscal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='fiscalizacao.nota_fiscal')),
            ],
        ),
        migrations.CreateModel(
            name='Cidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=60)),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='fiscalizacao.estado')),
            ],
            options={
                'ordering': ['nome'],
                'unique_together': {('estado', 'nome')},
            },
        ),
    ]
