# Generated by Django 3.0.3 on 2020-03-03 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20200303_1409'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='room',
            field=models.ForeignKey(db_column='Room', on_delete=django.db.models.deletion.CASCADE, to='main.Room'),
        ),
    ]
