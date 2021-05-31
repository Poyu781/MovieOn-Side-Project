# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class ActorMovieRelation(models.Model):
    actor = models.ForeignKey('ActorTable', models.DO_NOTHING)
    internal = models.ForeignKey('WebsIdRelation', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'actor_movie_relation'


class ActorTable(models.Model):
    actor_chinese_name = models.CharField(max_length=64)
    actor_english_name = models.CharField(max_length=64)
    mixed_name = models.CharField(max_length=125)

    class Meta:
        managed = False
        db_table = 'actor_table'


class DirectorMovieRelation(models.Model):
    director = models.ForeignKey('DirectorTable', models.DO_NOTHING)
    internal = models.ForeignKey('WebsIdRelation', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'director_movie_relation'


class DirectorTable(models.Model):
    director_chinese_name = models.CharField(max_length=64)
    director_english_name = models.CharField(max_length=64)
    mixed_name = models.CharField(max_length=125)

    class Meta:
        managed = False
        db_table = 'director_table'


class DoubanRating(models.Model):
    internal = models.ForeignKey('WebsIdRelation', models.DO_NOTHING)
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


class FeatureMovieTable(models.Model):
    feature = models.ForeignKey('FeatureTable', models.DO_NOTHING)
    internal = models.ForeignKey('WebsIdRelation', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'feature_movie_table'


class FeatureTable(models.Model):
    feature = models.CharField(max_length=16)

    class Meta:
        managed = True
        db_table = 'feature_table'


class ImdbRating(models.Model):
    internal = models.ForeignKey('WebsIdRelation', models.DO_NOTHING)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    rating_count = models.IntegerField()
    update_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'imdb_rating'


class InternalUserRating(models.Model):
    internal = models.ForeignKey('WebsIdRelation', models.DO_NOTHING)
    rating = models.IntegerField(blank=True, null=True)
    review_text = models.TextField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING,blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'internal_user_rating'


class LatestRating(models.Model):
    internal = models.ForeignKey('MovieBasicInfo', on_delete=models.CASCADE,to_field="internal",blank=True)
    audience_rating = models.CharField(max_length=16)
    tomator_rating = models.CharField(max_length=16)
    imdb_rating = models.DecimalField(max_digits=2, decimal_places=1)
    douban_rating = models.DecimalField(max_digits=2, decimal_places=1)
    internal_rating = models.DecimalField(max_digits=2, decimal_places=1)
    total_avg_rating = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        managed = True
        db_table = 'latest_rating'


class MovieBasicInfo(models.Model):
    internal = models.ForeignKey('WebsIdRelation',on_delete=models.CASCADE,unique=True,to_field="id")
    main_taiwan_name = models.CharField(max_length=125)
    main_original_name = models.CharField(max_length=125)
    is_adult = models.CharField(max_length=2)
    start_year = models.IntegerField()
    date_in_theater = models.DateField()
    runtime_minutes = models.IntegerField()
    img = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'movie_basic_info'


class MovieDescription(models.Model):
    internal = models.OneToOneField('WebsIdRelation', models.DO_NOTHING, primary_key=True)
    chinese_description = models.TextField()
    english_description = models.TextField()

    class Meta:
        managed = False
        db_table = 'movie_description'


class MovieOtherNames(models.Model):
    movie_name = models.CharField(max_length=64)
    internal = models.ForeignKey('WebsIdRelation', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'movie_other_names'


class RottenTomatoRating(models.Model):
    internal = models.ForeignKey('WebsIdRelation', models.DO_NOTHING)
    audience_rating = models.CharField(max_length=10)
    audience_rating_amount = models.CharField(max_length=64)
    tomator_rating = models.CharField(max_length=10)
    tomator_rating_amount = models.CharField(max_length=64)
    update_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'rotten_tomato_rating'


class WebsIdRelation(models.Model):
    imdb_id = models.CharField(unique=True, max_length=20, blank=True, null=True)
    douban_id = models.CharField(unique=True, max_length=20, blank=True, null=True)
    rotten_tomato_id = models.CharField(unique=True, max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'webs_id_relation'



class MovieDetail(models.Model):
    internal = models.IntegerField()
    imdb_rating = models.DecimalField(max_digits=2, decimal_places=1)
    imdb_rating = models.CharField(max_length=20)
# class CastTable(models.Model):
#     actor_name = models.CharField(max_length=64)
#     imdb_id = models.CharField(max_length=16)

#     class Meta:
#         managed = False
#         db_table = 'cast_table'
# class CategoryTable(models.Model):
#     feature = models.CharField(max_length=16)
#     imdb_id = models.CharField(max_length=16)

#     class Meta:
#         managed = False
#         db_table = 'category_table'


# class DirectorTable(models.Model):
#     director = models.CharField(max_length=16)
#     imdb_id = models.CharField(max_length=16)  # Field name made lowercase.

#     class Meta:
#         managed = False
#         db_table = 'director_table'



# class DoubanDetail(models.Model):
#     douban_id = models.CharField(max_length=16)
#     imdb_id = models.CharField(primary_key=True, max_length=16)
#     movie_title = models.CharField(max_length=64)
#     image = models.CharField(max_length=255)
#     other_names = models.CharField(max_length=255)
#     movie_description = models.TextField()

#     class Meta:
#         managed = True
#         db_table = 'douban_detail'


# class DoubanRating(models.Model):
#     douban_id = models.CharField(max_length=16)
#     imdb = models.ForeignKey('MovieDetail', models.DO_NOTHING)
#     avg_rating = models.DecimalField(max_digits=4, decimal_places=2)
#     five_star_ratio = models.DecimalField(max_digits=4, decimal_places=2)
#     four_star_ratio = models.DecimalField(max_digits=4, decimal_places=2)
#     three_star_ratio = models.DecimalField(max_digits=4, decimal_places=2)
#     two_star_ratio = models.DecimalField(max_digits=4, decimal_places=2)
#     one_star_ratio = models.DecimalField(max_digits=4, decimal_places=2)
#     total_rating_amount = models.IntegerField()
#     update_date = models.DateField()

#     class Meta:
#         managed = False
#         db_table = 'douban_rating'


# class ImdbRating(models.Model):
#     imdb = models.ForeignKey('MovieDetail', models.DO_NOTHING)
#     rating = models.DecimalField(max_digits=2, decimal_places=1)
#     rating_count = models.IntegerField()
#     update_date = models.DateField()

#     class Meta:
#         managed = False
#         db_table = 'imdb_rating'


# class MovieDetail(models.Model):
#     imdb_id = models.CharField(max_length=63)
#     primary_title = models.CharField(max_length=125)
#     original_title = models.CharField(max_length=125)
#     is_adult = models.CharField(max_length=2)
#     start_year = models.IntegerField()
#     runtime_minutes = models.IntegerField()
#     category = models.CharField(max_length=64)

#     class Meta:
#         managed = False
#         db_table = 'movie_detail'


# class LatestRating(models.Model):
#     # imdb_id = models.CharField(max_length=30)
#     imdb = models.ForeignKey('DoubanDetail', models.DO_NOTHING,related_name='keyword')
#     audience_rating = models.CharField(max_length=10)
#     tomator_rating = models.CharField(max_length=10)
#     imdb_rating = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
#     douban_rating = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'latest_rating'



# class RottenTomatoRating(models.Model):
#     rotten_tomato_id = models.CharField(max_length=20)
#     imdb_id = models.CharField(max_length=30)
#     audience_rating = models.CharField(max_length=10)
#     audience_rating_amount = models.CharField(max_length=64)
#     tomator_rating = models.CharField(max_length=10)
#     tomator_rating_amount = models.CharField(max_length=64)
#     update_date = models.DateField()

#     class Meta:
#         managed = False
#         db_table = 'rotten_tomato_rating'

# class InternalUserRating(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     movie_id = models.CharField(max_length=20,blank=True, null=True)
#     rating = models.IntegerField(blank=True, null=True)
#     update_date = models.DateTimeField(blank=True, null=True)
#     review_text = models.TextField(blank=True, null=True)
#     user = models.ForeignKey(User, models.DO_NOTHING,blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'internal_user_rating'