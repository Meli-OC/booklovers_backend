# Generated by Django 3.2 on 2021-06-01 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_keyword'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ('-published_date',)},
        ),
    ]
