# Generated by Django 5.0.4 on 2024-05-18 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_alter_borrowbook_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BorrowBook',
        ),
    ]
