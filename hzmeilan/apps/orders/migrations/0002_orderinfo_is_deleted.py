# Generated by Django 4.1.7 on 2023-07-25 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderinfo',
            name='is_deleted',
            field=models.BooleanField(default=False, help_text='是否删除', verbose_name='是否删除'),
        ),
    ]