# Generated by Django 3.0.3 on 2020-02-28 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20200228_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='cin_date',
            field=models.DateField(blank=True, db_column='CIN_Date', null=True, verbose_name='Check-In Date'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='cout_date',
            field=models.DateField(blank=True, db_column='COUT_Date', null=True, verbose_name='Check-Out Date'),
        ),
    ]
