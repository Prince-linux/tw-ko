# Generated by Django 3.2.9 on 2021-12-02 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='file',
            field=models.FileField(upload_to='uploads'),
        ),
    ]
