# Generated by Django 3.0.3 on 2020-02-28 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20200228_1558'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='room',
        ),
        migrations.AddField(
            model_name='booking',
            name='room_type',
            field=models.CharField(choices=[('S', 'Single Occupancy'), ('D', 'Double Occupancy'), ('F', 'Firemannsrom')], default=None, max_length=1),
        ),
    ]
