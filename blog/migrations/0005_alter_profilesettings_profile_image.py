# Generated by Django 4.0 on 2023-03-01 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_profilesettings_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilesettings',
            name='profile_image',
            field=models.FileField(blank=True, null=True, upload_to='images/'),
        ),
    ]
