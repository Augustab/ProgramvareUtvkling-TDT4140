# Generated by Django 3.0.3 on 2020-02-29 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20200228_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='room',
            field=models.ForeignKey(db_column='Room', default='100', on_delete=django.db.models.deletion.DO_NOTHING, to='main.Room'),
        ),
    ]
