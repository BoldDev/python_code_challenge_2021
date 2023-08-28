from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Title',
            fields=[
                ('imdb_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=120)),
                ('imdb_rating', models.FloatField(blank=True, null=True)),
                ('released', models.DateField(null=True)),
                ('runtime', models.CharField(blank=True, max_length=20, null=True)),
                ('director', models.CharField(blank=True, max_length=256, null=True)),
                ('plot', models.CharField(max_length=256)),
                ('language', models.CharField(blank=True, max_length=256, null=True)),
                ('country', models.CharField(blank=True, max_length=256, null=True)),
                ('poster', models.URLField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season_number', models.PositiveSmallIntegerField()),
                ('season_title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seasons', to='API.title')),
            ],
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('imdb_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=96)),
                ('episode_number', models.PositiveSmallIntegerField(help_text='This represents the episode number.', verbose_name='Episode number')),
                ('imdb_rating', models.CharField(blank=True, max_length=10, null=True)),
                ('released', models.DateField(blank=True, null=True)),
                ('episode_season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='episodes', to='API.season')),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=32)),
                ('comment', models.CharField(max_length=256)),
                ('created', models.DateTimeField(auto_now=True)),
                ('comment_episode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='API.episode')),
            ],
        ),
    ]
