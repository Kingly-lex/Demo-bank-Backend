# Generated by Django 5.0 on 2023-12-16 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0002_delete_accountnumbercheker'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllAcountNumbers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_no', models.CharField(max_length=255)),
            ],
        ),
    ]