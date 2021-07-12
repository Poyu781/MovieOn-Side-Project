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
    internal = models.ForeignKey('MovieBasicInfo', models.DO_NOTHING,to_field="internal")
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
    rating_total_amount = models.IntegerField()
    douban_rating_total_amount = models.IntegerField()

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
    publish_country = models.CharField(max_length=16)
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
    rotten_tomato_id = models.CharField(unique=True, max_length=125, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'webs_id_relation'


class MemberViewedRecord(models.Model):
    internal = models.ForeignKey('MovieBasicInfo', models.DO_NOTHING,to_field="internal")
    user_id = models.IntegerField()
    viewed_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'member_viewed_record'


class ErrorMsgRecord(models.Model):
    internal = models.ForeignKey('MovieBasicInfo', models.DO_NOTHING,to_field="internal")
    error_feature = models.CharField(max_length=30)
    error_message = models.TextField()
    user_id = models.IntegerField()
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'error_msg_record'


class UpdateMovieDetailPipelineData(models.Model):
    imdb_fetch_time = models.FloatField()
    new_imdb_amount = models.IntegerField()
    google_fetch_avg_time = models.FloatField()
    new_douban_amount = models.IntegerField()
    douban_fetch_avg_time = models.FloatField()
    douban_failed_amount = models.IntegerField()
    new_tomato_amount = models.IntegerField()
    tomato_fetch_avg_time = models.FloatField()
    tomato_failed_amount = models.IntegerField()
    insert_amount = models.IntegerField()
    insert_mysql_status = models.IntegerField()
    update_date = models.DateField()

    class Meta:
        managed = True
        db_table = 'update_movie_detail_pipeline_data'


class PipelineRatingStatus(models.Model):
    update_imdb_amount = models.IntegerField()
    not_rating_imdb_amount = models.IntegerField()
    update_douban_amount = models.IntegerField()
    not_rating_douban_amount = models.IntegerField()
    fail_douban_amount = models.IntegerField()
    update_tomato_amount = models.IntegerField()
    not_rating_tomato_amount = models.IntegerField()
    fail_tomato_amount = models.IntegerField()
    avg_douban_fetch_time = models.FloatField()
    avg_tomato_fetch_time = models.FloatField()
    update_date = models.DateField()

    class Meta:
        managed = True
        db_table = 'pipeline_rating_status'

class MovieRecommendList(models.Model):
    internal = models.ForeignKey(MovieBasicInfo, models.DO_NOTHING)
    recommend_list = models.CharField(max_length=125)

    class Meta:
        managed = True
        db_table = 'movie_recommend_list'