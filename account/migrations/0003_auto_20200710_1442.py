# Generated by Django 3.0.8 on 2020-07-10 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20200709_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='image_url',
            field=models.URLField(max_length=300, null=True),
        ),
    ]