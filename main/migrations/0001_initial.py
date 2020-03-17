<<<<<<< HEAD
# Generated by Django 3.0.3 on 2020-02-24 15:56
=======
# Generated by Django 3.0.3 on 2020-02-24 15:18
>>>>>>> origin/demo

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_no', models.CharField(max_length=5)),
                ('available', models.BooleanField(default=False)),
                ('capacity', models.IntegerField(default=None)),
                ('room_type', models.CharField(choices=[('S', 'Single Occupancy'), ('D', 'Double Occupancy'), ('B', 'Both Single and Double Occupancy')], default=None, max_length=1)),
            ],
        ),
    ]
