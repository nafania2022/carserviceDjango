# Generated by Django 4.2.1 on 2023-05-21 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carservice', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='serviceclient',
            old_name='data',
            new_name='date_service',
        ),
        migrations.AlterField(
            model_name='service',
            name='servicename',
            field=models.CharField(max_length=100),
        ),
    ]
