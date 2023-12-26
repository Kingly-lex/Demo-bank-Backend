# Generated by Django 5.0 on 2023-12-22 09:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_profiles', '0011_allacountnumbers'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AllAcountNumbers',
            new_name='AcountNumbers',
        ),
        migrations.AlterField(
            model_name='profile',
            name='account_no',
            field=models.TextField(blank=True, max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.TextField(max_length=100, null=True, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.TextField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Other', max_length=10),
        ),
        migrations.AlterField(
            model_name='profile',
            name='transfer_pin',
            field=models.TextField(default='1234', max_length=4, validators=[django.core.validators.MinLengthValidator(4)]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='verification_method',
            field=models.TextField(choices=[('NIN', 'NIN'), ('DRIVING_LICENCE', 'DRIVING_LICENCE'), ('PASSPORT', 'PASSPORT')], default='NIN', help_text='NIN, DRIVING_LICENCE, PASSPORT', max_length=50),
        ),
    ]