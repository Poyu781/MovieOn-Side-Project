# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils import timezone
class CategoryTable(models.Model):
    feature = models.CharField(max_length=16)
    imdb_id = models.CharField(max_length=16)

    class Meta:
        managed = False
        db_table = 'category_table'


class DirectorTable(models.Model):
    director = models.CharField(max_length=16)
    imdb_id = models.CharField(db_column='IMdb_id', max_length=16)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'director_table'



class DoubanDetail(models.Model):
    douban_id = models.CharField(primary_key=True, max_length=16)
    imdb_id = models.CharField(max_length=16)
    movie_title = models.CharField(max_length=64)
    image = models.CharField(max_length=255)
    other_names = models.CharField(max_length=255)
    movie_description = models.TextField()

    class Meta:
        managed = True
        db_table = 'douban_detail'


class DoubanRating(models.Model):
    douban_id = models.CharField(max_length=16)
    imdb = models.ForeignKey('MovieDetail', models.DO_NOTHING)
    avg_rating = models.DecimalField(max_digits=4, decimal_places=2)
    five_star_ratio = models.DecimalField(max_digits=4, decimal_places=2)
    four_star_ratio = models.DecimalField(max_digits=4, decimal_places=2)
    three_star_ratio = models.DecimalField(max_digits=4, decimal_places=2)
    two_star_ratio = models.DecimalField(max_digits=4, decimal_places=2)
    one_star_ratio = models.DecimalField(max_digits=4, decimal_places=2)
    total_rating_amount = models.IntegerField()
    update_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'douban_rating'


class ImdbRating(models.Model):
    imdb = models.ForeignKey('MovieDetail', models.DO_NOTHING)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    rating_count = models.IntegerField()
    update_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'imdb_rating'


class MovieDetail(models.Model):
    imdb_id = models.CharField(max_length=63)
    primary_title = models.CharField(max_length=125)
    original_title = models.CharField(max_length=125)
    is_adult = models.CharField(max_length=2)
    start_year = models.IntegerField()
    runtime_minutes = models.IntegerField()
    category = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'movie_detail'


class MovieLatestRating(models.Model):
    imdb_id = models.CharField(unique=True, max_length=30)
    title = models.CharField(max_length=125)
    imdb_rating = models.IntegerField()
    tomatoes_rating = models.IntegerField()
    douban_rating = models.IntegerField()
    ptt_rating = models.IntegerField()
    update_time = models.DateField(default = timezone.now())
    class Meta:
        managed = True
        db_table = 'movie_latest_rating'
class LatestRating(models.Model):
    imdb_id = models.CharField(max_length=30)
    audience_rating = models.CharField(max_length=10)
    tomator_rating = models.CharField(max_length=10)
    imdb_rating = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    douban_rating = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'latest_rating'
# class RottenTomatoRating(models.Model):
#     tomato_id = models.CharField(max_length=16)
#     imdb_id = models.CharField(unique=True, max_length=26)
#     title = models.CharField(max_length=125)
#     imdb_rating = models.IntegerField()
#     tomatoes_rating = models.IntegerField()
#     douban_rating = models.IntegerField()
#     ptt_rating = models.IntegerField()