# Generated by Django 4.2.5 on 2023-09-20 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='username',
            field=models.CharField(default='', max_length=30, unique=True),
        ),
    ]