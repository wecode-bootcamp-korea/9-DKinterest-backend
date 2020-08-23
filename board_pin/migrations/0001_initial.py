# Generated by Django 3.1a1 on 2020-08-23 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=5000)),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('secret', models.BooleanField(null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.account')),
            ],
            options={
                'db_table': 'boards',
            },
        ),
        migrations.CreateModel(
            name='Pin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField(max_length=300)),
                ('title', models.CharField(max_length=5000, null=True)),
                ('detail', models.CharField(max_length=5000, null=True)),
                ('link', models.CharField(max_length=5000, null=True)),
                ('comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.comment')),
                ('external_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sharer_pin', to='account.account')),
                ('interest', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.interest')),
                ('internal_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='uploader_pin', to='account.account')),
            ],
            options={
                'db_table': 'pins',
            },
        ),
        migrations.CreateModel(
            name='BoardPin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='board_pin.board')),
                ('pin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='board_pin.pin')),
            ],
            options={
                'db_table': 'board_pins',
            },
        ),
        migrations.AddField(
            model_name='board',
            name='pin',
            field=models.ManyToManyField(through='board_pin.BoardPin', to='board_pin.Pin'),
        ),
        migrations.CreateModel(
            name='AccountBoardPin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.account')),
                ('board_pin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='board_pin.boardpin')),
            ],
            options={
                'db_table': 'account_board_pins',
            },
        ),
    ]
