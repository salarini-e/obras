# Generated by Django 3.2.12 on 2022-07-22 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fiscalizacao', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='obra',
            name='data_conclusao',
            field=models.DateField(blank=True, null=True, verbose_name='Data prevista de conclusão'),
        ),
    ]
