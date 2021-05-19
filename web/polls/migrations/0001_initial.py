# Generated by Django 3.2.3 on 2021-05-19 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.CharField(max_length=16)),
                ('imdb_id', models.CharField(max_length=16)),
            ],
            options={
                'db_table': 'category_table',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DirectorTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('director', models.CharField(max_length=16)),
                ('imdb_id', models.CharField(db_column='IMdb_id', max_length=16)),
            ],
            options={
                'db_table': 'director_table',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DoubanDetail',
            fields=[
                ('douban_id', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('imdb_id', models.CharField(max_length=16)),
                ('movie_title', models.CharField(max_length=64)),
                ('image', models.CharField(max_length=255)),
                ('other_names', models.CharField(max_length=255)),
                ('movie_description', models.TextField()),
            ],
            options={
                'db_table': 'douban_detail',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DoubanRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('douban_id', models.CharField(max_length=16)),
                ('avg_rating', models.DecimalField(decimal_places=2, max_digits=4)),
                ('five_star_ratio', models.DecimalField(decimal_places=2, max_digits=4)),
                ('four_star_ratio', models.DecimalField(decimal_places=2, max_digits=4)),
                ('three_star_ratio', models.DecimalField(decimal_places=2, max_digits=4)),
                ('two_star_ratio', models.DecimalField(decimal_places=2, max_digits=4)),
                ('one_star_ratio', models.DecimalField(decimal_places=2, max_digits=4)),
                ('total_rating_amount', models.IntegerField()),
                ('update_date', models.DateField()),
            ],
            options={
                'db_table': 'douban_rating',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ImdbRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2)),
                ('rating_count', models.IntegerField()),
                ('update_date', models.DateField()),
            ],
            options={
                'db_table': 'imdb_rating',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MovieDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imdb_id', models.CharField(max_length=63)),
                ('primary_title', models.CharField(max_length=125)),
                ('original_title', models.CharField(max_length=125)),
                ('is_adult', models.CharField(max_length=2)),
                ('start_year', models.IntegerField()),
                ('runtime_minutes', models.IntegerField()),
                ('category', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'movie_detail',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MovieLatestRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imdb_id', models.CharField(max_length=26, unique=True)),
                ('title', models.CharField(max_length=125)),
                ('imdb_rating', models.IntegerField()),
                ('tomatoes_rating', models.IntegerField()),
                ('douban_rating', models.IntegerField()),
                ('ptt_rating', models.IntegerField()),
            ],
            options={
                'db_table': 'movie_latest_rating',
                'managed': False,
            },
        ),
    ]
