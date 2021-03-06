# Generated by Django 3.1.5 on 2021-02-17 08:10

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('place_id', models.AutoField(primary_key=True, serialize=False)),
                ('city', models.CharField(max_length=50, verbose_name='Ville')),
                ('zipcode', models.CharField(max_length=5, validators=[django.core.validators.MinLengthValidator(5)], verbose_name='Code Postal')),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
            ],
            options={
                'unique_together': {('city', 'zipcode')},
            },
        ),
        migrations.CreateModel(
            name='PermutSearch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('place_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='permut_creation.place')),
            ],
            options={
                'unique_together': {('place_id', 'email')},
            },
        ),
    ]
