# Generated by Django 4.1.5 on 2023-01-31 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0004_rename_is_parent_comment_parent"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="views",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
