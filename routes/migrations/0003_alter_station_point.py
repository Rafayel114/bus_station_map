# Generated by Django 3.2.17 on 2023-02-11 13:40

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0002_auto_20230211_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
    ]
