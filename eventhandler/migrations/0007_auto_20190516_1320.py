# Generated by Django 2.1.5 on 2019-05-16 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eventhandler', '0006_auto_20190516_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventrecord',
            name='specode',
            field=models.ForeignKey(db_column='specode', on_delete=django.db.models.deletion.DO_NOTHING, to='eventhandler.EventType', to_field='code'),
        ),
    ]
