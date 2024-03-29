# Generated by Django 4.2.5 on 2023-12-29 22:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("dictionary", "0003_alter_historicalpartofspeech_code_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wordpair",
            name="part_of_speech",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="dictionary.partofspeech",
            ),
        ),
        migrations.AlterField(
            model_name="wordpair",
            name="root",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="children",
                to="dictionary.wordpair",
            ),
        ),
    ]
