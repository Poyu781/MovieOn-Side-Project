from .models import MovieBasicInfo,LatestRating,WebsIdRelation,FeatureMovieTable,FeatureTable #DoubanDetail,LatestRating,
from rest_framework import serializers

# class DoubanDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DoubanDetail
#         fields = '__all__'
# class LatestRatingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LatestRating
#         fields = '__all__'
#         depth = 1


class Web(serializers.ModelSerializer):
    # chinese_name = serializers.SerializerMethodField("get_cn_name_from_basic")
    # english_name = serializers.SerializerMethodField("get_eg_name_from_basic")
    class Meta:
        model = WebsIdRelation
        field = "__all__"
class MovieBasicSerializer(serializers.ModelSerializer):
    # movie = Web(many=True, read_only=True)
    # id_relate = serializers.HyperlinkedRelatedField(
    #     many=False,
    #     read_only=True,
    #     view_name='id_relate-detail'
    # )

    class Meta:
        model = MovieBasicInfo
        fields = "__all__"

    def get_rating_from_last(self,movie_basic_info):
        rating = movie_basic_info.internal.imdb_rating
        return rating
class FlattenMixin(object):
    """Flatens the specified related objects in this representation"""
    def to_representation(self, obj):
        assert hasattr(self.Meta, 'flatten'), (
            'Class {serializer_class} missing "Meta.flatten" attribute'.format(
                serializer_class=self.__class__.__name__
            )
        )
        # Get the current object representation
        rep = super(FlattenMixin, self).to_representation(obj)
        # Iterate the specified related objects with their serializer
        for field, serializer_class in self.Meta.flatten:
            serializer = serializer_class(context = self.context)
            objrep = serializer.to_representation(getattr(obj, field))
            #Include their fields, prefixed, in the current   representation
            for key in objrep:
                rep[key] = objrep[key]
        return rep
class LastestInfoSerializer(serializers.ModelSerializer):
    internal = MovieBasicSerializer()
    # chinese_name = serializers.SerializerMethodField("get_cn_name_from_basic")
    # english_name = serializers.SerializerMethodField("get_eg_name_from_basic")
    # movie = MovieBasicSerializer(many=True, read_only=True)
    class Meta:
        model = LatestRating
        # fields = ("internal_id",'audience_rating',"imdb_rating", "tomator_rating","douban_rating","chinese_name","english_name")
        fields = "__all__"
        # flatten = [ ('internal', MovieBasicSerializer) ]

    def to_representation(self, obj):
        """Move fields from profile to user representation."""
        representation = super().to_representation(obj)
        profile_representation = representation.pop('internal')
        for key in profile_representation:
            representation[key] = profile_representation[key]

        return representation
    # def setup_eager_loading(cls, queryset):
    #     """ Perform necessary eager loading of data. """
    #     queryset = queryset.prefetch_related('movie')
    #     return queryset
        # flatten = [ ('internal', MovieBasicSerializer) ]
    # def get_cn_name_from_basic(self,obj):
    #     cn_name = obj.internal.main_taiwan_name
    #     return cn_name
    # def get_eg_name_from_basic(self,obj):
    #     cn_name = obj.internal.main_original_name
    #     return cn_name




    # 
    # tracks = LastestRatingSerializer( read_only=True,source='test')
class FeaNaSer(serializers.ModelSerializer):  
    class Meta:
        model = FeatureTable
        fields = "__all__"
class FeaSer(serializers.ModelSerializer):  
    feature = FeaNaSer()
    class Meta:
        model = FeatureMovieTable
        fields = "__all__"

    def to_representation(self, obj):
        """Move fields from profile to user representation."""
        representation = super().to_representation(obj)
        profile_representation = representation.pop('feature')
        for key in profile_representation:
            representation[key] = profile_representation[key]

        return representation

# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ('phone', 'some', 'other', 'fields')


# class UserDetailsSerializer(serializers.ModelSerializer):
#     """User model with Profile. Handled as a single object, profile is flattened."""
#     profile = ProfileSerializer()

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'profile')
#         read_only_fields = ('email', )



#     def to_internal_value(self, data):
#         """Move fields related to profile to their own profile dictionary."""
#         profile_internal = {}
#         for key in ProfileSerializer.Meta.fields:
#             if key in data:
#                 profile_internal[key] = data.pop(key)

#         internal = super().to_internal_value(data)
#         internal['profile'] = profile_internal
#         return internal

#     def update(self, instance, validated_data):
#         """Update user and profile. Assumes there is a profile for every user."""
#         profile_data = validated_data.pop('profile')
#         super().update(instance, validated_data)

#         profile = instance.profile
#         for attr, value in profile_data.items():
#             setattr(profile, attr, value)
#         profile.save()

#         return instance