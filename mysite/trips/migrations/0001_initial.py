# Generated by Django 2.2.9 on 2020-02-13 08:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, unique=True)),
                ('content', models.TextField()),
                ('pubDateTime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-pubDateTime'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=128)),
                ('pubDateTime', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trips.Article')),
            ],
            options={
                'ordering': ['pubDateTime'],
            },
        ),
    ]
