# Generated by Django 3.1.5 on 2021-01-28 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jogo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criador', models.CharField(max_length=512, null=True)),
                ('esporte', models.CharField(max_length=512, null=True)),
                ('data', models.CharField(max_length=512, null=True)),
                ('horas', models.CharField(max_length=512, null=True)),
                ('descricao', models.CharField(max_length=512)),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='static')),
            ],
        ),
        migrations.DeleteModel(
            name='Todo',
        ),
    ]
