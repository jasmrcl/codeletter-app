# Generated by Django 4.0 on 2023-03-01 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_comment_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilesettings',
            name='profile_image',
            field=models.FileField(blank=True, null=True, upload_to='images/'),
        ),
    ]
