# Generated by Django 2.2.3 on 2021-02-24 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contatos', '0002_contato_mostrar'),
    ]

    operations = [
        migrations.AddField(
            model_name='contato',
            name='foto',
            field=models.ImageField(blank=True, upload_to='pictures/%Y/%m/%d'),
        ),
    ]
