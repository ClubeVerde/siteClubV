# Generated by Django 5.1.6 on 2025-02-12 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_pedido_quantidade_alter_pedido_assinatura'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='status',
            field=models.CharField(choices=[('pendente', 'Pendente'), ('pago', 'Pago'), ('cancelado', 'Cancelado')], default='pendente', max_length=255),
        ),
    ]
