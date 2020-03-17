# Generated by Django 3.0.3 on 2020-02-28 14:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room_type',
            field=models.CharField(choices=[('S', 'Single Occupancy'), ('D', 'Double Occupancy'), ('F', 'Firemannsrom')], default=None, max_length=1),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('bookingid', models.AutoField(db_column='BookingID', primary_key=True, serialize=False)),
                ('cin_date', models.DateTimeField(blank=True, db_column='CIN_Date', null=True, verbose_name='Check-In Date')),
                ('cout_date', models.DateTimeField(blank=True, db_column='COUT_Date', null=True, verbose_name='Check-Out Date')),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('room', models.ForeignKey(db_column='Room', default='1', on_delete=django.db.models.deletion.DO_NOTHING, to='main.Room')),
            ],
            options={
                'db_table': 'Booking',
                'managed': True,
            },
        ),
    ]
