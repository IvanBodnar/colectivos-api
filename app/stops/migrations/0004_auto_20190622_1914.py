# Generated by Django 2.2.2 on 2019-06-22 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stops', '0003_auto_20190622_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stops',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]