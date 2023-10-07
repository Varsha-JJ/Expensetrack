# Generated by Django 4.2.5 on 2023-10-07 07:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expense_name', models.CharField(help_text='Expense name/description', max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, help_text='Amount spent', max_digits=10)),
                ('transaction_date', models.DateField(default=django.utils.timezone.now, help_text='Date of transaction')),
                ('category', models.CharField(choices=[('Food', 'Food'), ('Transportation', 'Transportation'), ('Entertainment', 'Entertainment'), ('Other', 'Other')], help_text='Category of expense', max_length=20)),
            ],
        ),
    ]
