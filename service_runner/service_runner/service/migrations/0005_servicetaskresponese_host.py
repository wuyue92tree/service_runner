# Generated by Django 2.2.6 on 2019-10-23 09:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0004_auto_20191014_0953'),
        ('service', '0004_auto_20191023_1704'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicetaskresponese',
            name='host',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='asset.Host', verbose_name='Host'),
        ),
    ]
