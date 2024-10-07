# Generated by Django 5.1.1 on 2024-10-06 10:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("frameit", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="job",
            name="special_instructions",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="jobcomponent",
            name="type",
            field=models.CharField(
                choices=[("frame", "Frame"), ("mat", "Mat"), ("glass", "Glass")],
                max_length=10,
            ),
        ),
    ]
