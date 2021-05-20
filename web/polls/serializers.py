from .models import DoubanDetail,LatestRating
from rest_framework import serializers

class DoubanDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoubanDetail
        fields = '__all__'
class LatestRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = LatestRating
        fields = '__all__'
        depth = 1