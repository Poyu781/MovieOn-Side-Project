from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.http import HttpResponse
# from .models import DoubanDetail,LatestRating,InternalUserRating
from django.db import transaction
from rest_framework import viewsets
from rest_framework import generics
from .serializers import MovieBasicSerializer,LastestInfoSerializer,FeaSer
from .models import MovieBasicInfo,LatestRating,FeatureMovieTable,FeatureTable,InternalUserRating,MovieOtherNames
# from .serializers import DoubanDetailSerializer ,LatestRatingSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from .forms import RegisterForm,LoginForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import json
from django.contrib import messages
from datetime import datetime
from pandas.io.json import json_normalize
from rest_framework.decorators import api_view
from .models import MovieDetail
from django.db import connection

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

@api_view(['GET'])
def test(request,format=None,):
    cursor= connection.cursor()
    cursor.execute('')
    result = dictfetchall(cursor)
    # print(type(result))
    # # r = {"test":12}
    # # result[0].update(r)
    print(result)
    return Response(result)
@api_view(['GET'])
def show_detail(request,internal_id,format=None,):
    print(internal_id)
    cursor= connection.cursor()
    cursor.execute(f"CALL `get_movie_detail_procedure`({int(internal_id)})")
    result = dictfetchall(cursor)
    cursor.execute(f"CALL `get_director_actor_feature`({int(internal_id)})")
    # x = dictfetchall(cursor)
    # print(x)
    result[0].update(dictfetchall(cursor)[0])
    # print(type(result))
    # # r = {"test":12}
    # # result[0].update(r)
    # print(result)
    return Response(result)

@api_view(['GET'])
def get_home_page_data(request, format=None):
    if request.method == 'GET':
        feature = request.GET.get('feature')
        start_num = int(request.GET.get('start',0))
        movie_info = LatestRating.objects.select_related("internal").order_by("internal__start_year").reverse()
        if feature:
            id_result = FeatureMovieTable.objects.values("internal_id").filter(feature_id=feature)
            print(id_result)
            result = movie_info.filter(internal_id__in =id_result)
        else:
            result = movie_info
        count = result.count()
        # print(start_num)
        # print(count)
        serializer = LastestInfoSerializer(result[start_num:min(start_num+20,count)], many=True)
        # print(type(serializer.data))
        # print(serializer)
        return Response(serializer.data)

@api_view(['GET'])
def search_movie(request, format=None):
    if request.method == 'GET':
        query = request.GET.get('query')

        movie_info = LatestRating.objects.select_related("internal")
        id_result = MovieOtherNames.objects.values("internal_id").filter(movie_name__icontains=query)
        print(id_result)
        result = movie_info.filter(internal_id__in =id_result).order_by("internal__start_year").reverse()
        # print(id_result)
        # print(count)
        serializer = LastestInfoSerializer(result, many=True)
        # print(type(serializer.data))
        # print(serializer)
        return Response(serializer.data)
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def main_page(request):
    # print(DoubanDetail.objects.filter(douban_id__contains="7916239")[0].movie_title)

    return render(request,"home_page.html")

@login_required
def member_page(request):
    return render(request,"member_page.html")

# @login_required
def movie_single_page(request,internal_id):
    current_user = request.user
    content = {}
    try :
        review = InternalUserRating.objects.get(user_id = current_user.id, internal_id= internal_id)
        content['rating']=review.rating
    except:
        content['rating'] = ""
        pass
    print(content)
    return render(request,"movie_page.html",content)

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
        print(user)
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
    # review_record = InternalUserRating.objects.filter(user_id = current_user.id, movie_id= imdb_id)
    # if review_record.exists():
    try:
        review = InternalUserRating.objects.get(user_id = current_user.id, internal_id= imdb_id)
        print(review)
        review.rating = rating
        review.update_date = datetime.now()
    except:
        review = InternalUserRating(internal_id = imdb_id, update_date = datetime.now(), rating = rating, user_id = current_user.id)
        print(1)
    review.save()
    # print(review_record)

    return JsonResponse({"message":"success"})


def logout(request):
    auth.logout(request)
    return redirect('/')