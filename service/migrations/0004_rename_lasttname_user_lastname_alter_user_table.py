# Generated by Django 4.0.3 on 2022-04-11 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_alter_user_table'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='lasttName',
            new_name='lastName',
        ),
        migrations.AlterModelTable(
            name='user',
            table='sos_user',
        ),
    ]
