from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from .models import DoubanDetail,LatestRating
from django.db import transaction
from rest_framework import viewsets
from .serializers import DoubanDetailSerializer ,LatestRatingSerializer

class DoubanDetailView(viewsets.ModelViewSet):
    queryset = DoubanDetail.objects.all()
    serializer_class = DoubanDetailSerializer
class LatestRatingView(viewsets.ModelViewSet):
    queryset = LatestRating.objects.all()
    serializer_class = LatestRatingSerializer


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def main_page(request):
    # print(DoubanDetail.objects.filter(douban_id__contains="7916239")[0].movie_title)
    return render(request,"index.html")


def get_movies_rating(request):
    data = DoubanDetail.objects.get(douban_id= "10001432")
    ro = LatestRating.objects.get(imdb_id = "tt8096832")
    total = LatestRating.objects.select_related('imdb').all()
    # print(total)
    for i in total:
        print("33")
        print(i)
        break
    # print()
    return HttpResponse(f"{total.query}")