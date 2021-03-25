# Generated by Django 3.1.7 on 2021-03-25 20:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('show', '0005_episode_imdb_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('episode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='show.episode')),
            ],
        ),
    ]
