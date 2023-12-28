# Generated by Django 5.0 on 2023-12-28 21:58

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0011_rename_comment_deposit_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('pkid', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sender', models.TextField(max_length=20, verbose_name='Sender Account Number')),
                ('receiver', models.TextField(max_length=20, verbose_name='Receiver Account Number')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('type', models.TextField(choices=[('Transfer', 'Transfer'), ('Withdrawal', 'Withdrawal'), ('Deposit', 'Deposit')], default='Transfer', max_length=20)),
                ('processed_by', models.TextField(default='Auto-transfer', max_length=100, verbose_name='Banker id')),
                ('charge', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('description', models.TextField(blank=True, max_length=200, null=True)),
                ('is_successful', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='deposit',
            name='processed_by',
        ),
        migrations.DeleteModel(
            name='Transfer',
        ),
        migrations.RemoveField(
            model_name='withdrawal',
            name='processed_by',
        ),
        migrations.DeleteModel(
            name='Deposit',
        ),
        migrations.DeleteModel(
            name='Withdrawal',
        ),
    ]