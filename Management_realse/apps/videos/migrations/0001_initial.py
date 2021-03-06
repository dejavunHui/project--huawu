# Generated by Django 2.1.1 on 2018-10-04 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=30, null=True)),
                ('name', models.CharField(max_length=20)),
                ('year', models.IntegerField(verbose_name='年份')),
                ('info', models.TextField()),
                ('img', models.URLField(null=True)),
                ('sr_video', models.URLField()),
                ('x2_video', models.URLField(null=True)),
                ('x3_video', models.URLField(null=True)),
                ('x4_video', models.URLField(null=True)),
                ('flag', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': '视频信息',
                'verbose_name_plural': '视频信息',
                'db_table': 'app_videos',
            },
        ),
    ]
