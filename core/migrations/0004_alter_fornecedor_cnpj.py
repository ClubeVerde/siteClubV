# Generated by Django 5.1.6 on 2025-02-07 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_fornecedor_email_fornecedor_cnpj_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fornecedor',
            name='cnpj',
            field=models.CharField(default='00000000000000', max_length=14),
        ),
    ]
