from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from .models import DoubanDetail,LatestRating
from django.db import transaction
from rest_framework import viewsets
from .serializers import DoubanDetailSerializer ,LatestRatingSerializer
from django_filters.rest_framework import DjangoFilterBackend
class DoubanDetailView(viewsets.ModelViewSet):
    queryset = DoubanDetail.objects.all()
    serializer_class = DoubanDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['imdb_id']
class LatestRatingView(viewsets.ModelViewSet):
    queryset = LatestRating.objects.all().select_related('imdb')
    serializer_class = LatestRatingSerializer


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def main_page(request):
    # print(DoubanDetail.objects.filter(douban_id__contains="7916239")[0].movie_title)
    
    return render(request,"index.html")

def movie_single_page(request,imdb_id):
    data = DoubanDetail.objects.filter(imdb_id= imdb_id)
    
    return render(request,"movie_page.html",list(data.values())[0])

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

