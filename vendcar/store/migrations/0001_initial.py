# Generated by Django 2.1.4 on 2018-12-08 13:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Acessorio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Carro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelo', models.CharField(max_length=100)),
                ('ano_modelo', models.CharField(max_length=4)),
                ('ano_fabricacao', models.CharField(max_length=4)),
                ('nume_portas', models.IntegerField(default=2)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='media/')),
            ],
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('sigle', models.CharField(max_length=3)),
            ],
        ),
        migrations.AddField(
            model_name='carro',
            name='marca',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carros', to='store.Marca'),
        ),
        migrations.AddField(
            model_name='carro',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meus_carros', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='acessorio',
            name='carro',
            field=models.ManyToManyField(to='store.Carro'),
        ),
    ]