# Generated by Django 3.1.5 on 2021-02-17 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permut_creation', '0002_auto_20210217_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='lat',
            field=models.DecimalField(blank=True, decimal_places=16, max_digits=19, null=True),
        ),
        migrations.AlterField(
            model_name='place',
            name='lng',
            field=models.DecimalField(blank=True, decimal_places=16, max_digits=19, null=True),
        ),
    ]
