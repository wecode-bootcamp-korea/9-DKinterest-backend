# Generated by Django 3.1a1 on 2020-09-20 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100, null=True, unique=True)),
                ('password', models.CharField(max_length=500, null=True)),
                ('nickname', models.CharField(max_length=100, null=True, unique=True)),
                ('age', models.IntegerField(null=True)),
                ('name', models.CharField(max_length=50)),
                ('follower_number', models.IntegerField(default=0)),
                ('image_url', models.URLField(max_length=300, null=True)),
            ],
            options={
                'db_table': 'accounts',
            },
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'genders',
            },
        ),
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image_url', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'interests',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'languages',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'regions',
            },
        ),
        migrations.CreateModel(
            name='SocialPlatform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'social_platforms',
            },
        ),
        migrations.CreateModel(
            name='Following',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_following', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='follower', to='account.account')),
                ('to_following', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='followee', to='account.account')),
            ],
            options={
                'db_table': 'followings',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=1000)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comment', to='account.account')),
                ('mother_comment', models.ForeignKey(blank=True, max_length=1000, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='account.comment')),
            ],
            options={
                'db_table': 'comments',
            },
        ),
        migrations.CreateModel(
            name='AccountInterest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.account')),
                ('interest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.interest')),
            ],
            options={
                'db_table': 'account_interests',
            },
        ),
        migrations.CreateModel(
            name='AccountCommentLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.account')),
                ('comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.comment')),
            ],
            options={
                'db_table': 'account_comment_likes',
            },
        ),
    ]
