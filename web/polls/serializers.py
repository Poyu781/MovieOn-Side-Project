from .models import MovieBasicInfo, LatestRating, WebsIdRelation, InternalUserRating, MemberViewedRecord,PipelineRatingStatus,UpdateMovieDetailPipelineData
from rest_framework import serializers


class Web(serializers.ModelSerializer):
    class Meta:
        model = WebsIdRelation
        field = "__all__"


class MovieBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieBasicInfo
        fields = "__all__"

class RatingPipelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = PipelineRatingStatus
        fields = "__all__"

class MovieUpdatePipelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpdateMovieDetailPipelineData
        fields = "__all__"

class MovieBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieBasicInfo
        fields = "__all__"

class LastestInfoSerializer(serializers.ModelSerializer):
    internal = MovieBasicSerializer()

    class Meta:
        model = LatestRating
        fields = "__all__"

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        profile_representation = representation.pop('internal')
        for key in profile_representation:
            representation[key] = profile_representation[key]
        return representation



class InternalUserRatingSerializer(serializers.ModelSerializer):
    internal = MovieBasicSerializer()

    class Meta:
        model = InternalUserRating
        fields = "__all__"

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        profile_representation = representation.pop('internal')
        for key in profile_representation:
            representation[key] = profile_representation[key]
        return representation


class MemberViewedRecordSerializer(serializers.ModelSerializer):
    internal = MovieBasicSerializer()

    class Meta:
        model = MemberViewedRecord
        fields = "__all__"

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        profile_representation = representation.pop('internal')
        for key in profile_representation:
            representation[key] = profile_representation[key]
        return representation
