# Generated by Django 3.1.5 on 2021-02-13 02:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Banker', '0006_auto_20210212_0517'),
    ]

    operations = [
        migrations.AddField(
            model_name='registercustomers',
            name='id',
            field=models.ForeignKey(default=11, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]
