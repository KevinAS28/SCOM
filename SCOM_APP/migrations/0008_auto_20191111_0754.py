# Generated by Django 2.2.4 on 2019-11-11 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SCOM_APP', '0007_auto_20191111_0704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infoguru',
            name='nama',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='infoguru',
            name='nip',
            field=models.CharField(max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='infosiswa',
            name='nis',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]