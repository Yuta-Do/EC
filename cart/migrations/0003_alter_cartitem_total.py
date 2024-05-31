# Generated by Django 5.0.6 on 2024-05-28 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_cartitem_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='total',
            field=models.DecimalField(decimal_places=0, default=0, editable=False, max_digits=10),
        ),
    ]