from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.http import HttpResponse
from .models import DoubanDetail,LatestRating,InternalUserRating
from django.db import transaction
from rest_framework import viewsets
from .serializers import DoubanDetailSerializer ,LatestRatingSerializer
from django_filters.rest_framework import DjangoFilterBackend

from .forms import RegisterForm,LoginForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import json
from django.contrib import messages
from datetime import datetime
class DoubanDetailView(viewsets.ModelViewSet):
    queryset = DoubanDetail.objects.all()
    serializer_class = DoubanDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['imdb_id']
class LatestRatingView(viewsets.ModelViewSet):
    queryset = LatestRating.objects.all().select_related('imdb')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['imdb_id']
    serializer_class = LatestRatingSerializer


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def main_page(request):
    # print(DoubanDetail.objects.filter(douban_id__contains="7916239")[0].movie_title)

    return render(request,"home_page.html")


# @login_required
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

def sign_up(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = request.POST.get('username')
            pwd = request.POST.get('password1')
            # if 驗證成功返回 user 物件，否則返回None
            user = auth.authenticate(username=user, password=pwd)
            auth.login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get("next"))
            return redirect('/')  #重新導向到登入畫面
    context = {
        'form': form
    }
    return render(request, 'sign_up.html', context)

def sign_in(request):
    form = LoginForm()
    context = {
        'form': form
    }
    if request.method == 'POST':
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        # if 驗證成功返回 user 物件，否則返回None
        user = auth.authenticate(username=user, password=pwd)

        if user:
            # request.user ： 當前登入物件
            auth.login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get("next"))
            else:
            # return HttpResponse("OK")
                return redirect('/')
        else:
            messages.error(request,'username or password not correct')
            return redirect('/signin')
    return render(request, 'sign_in.html', context)

# def login(request):
#     username = request.user.username    
#     return render(request, 'user_page.html', locals())


@login_required
def score_movie(request):
    current_user = request.user
    get_dict = json.load(request)
    rating = get_dict['rating']
    imdb_id = get_dict['imdb_id']
    review_record = InternalUserRating.objects.filter(user_id = current_user.id, movie_id= imdb_id)
    if review_record.exists():
        review = InternalUserRating.objects.get(user_id = current_user.id, movie_id= imdb_id)
        print(review)
        review.rating = rating
        review.update_date = datetime.now()
    else:
        review = InternalUserRating(movie_id = imdb_id, update_date = datetime.now(), rating = rating, user_id = current_user.id)
        print(1)
    review.save()
    # print(review_record)

    return JsonResponse({"message":"success"})


def logout(request):
    auth.logout(request)
    return redirect('/')