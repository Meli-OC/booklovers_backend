# Generated by Django 3.2 on 2021-05-12 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_auto_20210512_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='author_name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
