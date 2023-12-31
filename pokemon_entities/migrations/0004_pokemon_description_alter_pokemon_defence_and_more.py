# Generated by Django 4.2.3 on 2023-08-03 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0003_pokemon_defence_pokemon_health_pokemon_level_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='description',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='defence',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='health',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='level',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='stamina',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='strength',
            field=models.IntegerField(blank=True),
        ),
    ]
