# Generated by Django 3.2.19 on 2024-03-14 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Routine', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='classroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Routine.class'),
        ),
    ]
