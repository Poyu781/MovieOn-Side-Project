## Django module
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages

## API relation
from rest_framework.decorators import api_view,permission_classes
from .models import MovieBasicInfo, LatestRating, FeatureMovieTable, FeatureTable, InternalUserRating, MovieOtherNames, InternalUserRating, MemberViewedRecord, ErrorMsgRecord
from .serializers import MovieBasicSerializer, LastestInfoSerializer, InternalUserRatingSerializer, MemberViewedRecordSerializer
from rest_framework.response import Response
from django.db import connection
from rest_framework.permissions import IsAuthenticated

## others
from .forms import RegisterForm, LoginForm
import json
from datetime import datetime
from functools import wraps
import time, redis
from statistics import mean, pstdev
from collections import defaultdict
redis = redis.Redis(host='localhost', port=6379, db=0)

def rate_limiter(fun):
    @wraps(fun)
    def decorated(*args,**kwargs):
        ip_address = args[0].META['REMOTE_ADDR']
        redis.set(ip_address,0,ex=60,nx=True)
        redis.incr(ip_address)
        if int(redis.get(ip_address)) >= 100 :
            return HttpResponse('Your request has exceeded the allowed quantity', 429)
        return fun(*args,**kwargs)
    return decorated

# Render with html 
def advanced_search_page(request):
    return render(request, "advanced_search_page.html")


def search_by_word_page(request):
    return render(request, "search_by_word_page.html")


def main_page(request):
    return render(request, "home_page.html")


def movie_single_page(request, internal_id):
    content = {}
    if str(request.user) != "AnonymousUser":
        current_user = request.user
        try:
            review = MemberViewedRecord.objects.get(user_id=current_user.id,
                                                    internal_id=internal_id)
            review.viewed_date = datetime.now()
            review.save()
        except:
            try:
                review = MemberViewedRecord(internal_id=internal_id,
                                            viewed_date=datetime.now(),
                                            user_id=current_user.id)
                review.save()
            except:
                return render(request, "movie_page.html")
        

        try:
            review = InternalUserRating.objects.get(user_id=current_user.id,
                                                    internal_id=internal_id)
            content['rating'] = review.rating
        except:
            content['rating'] = ""
        return render(request, "movie_page.html", content)
    content['rating'] = ""
    return render(request, "movie_page.html", content)


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
    context = {'form': form}
    return render(request, 'sign_up.html', context)


def sign_in(request):
    form = LoginForm()
    context = {'form': form}
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
            messages.error(request, 'username or password not correct')
            return redirect('/signin')
    return render(request, 'sign_in.html', context)


@login_required
def member_page(request):
    return render(request, "member_page.html")


## API

def dict_fetch_all(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


@rate_limiter
@api_view(['GET'])
def get_movie_detail_info(request, internal_id, format=None):
    try :
        cursor = connection.cursor()
        cursor.execute(f"CALL `get_movie_detail_procedure`({int(internal_id)})")
        result = dict_fetch_all(cursor)
        cursor.execute(f"CALL `get_director_actor_feature`({int(internal_id)})")
        result[0].update(dict_fetch_all(cursor)[0])
        return Response(result)
    except:
        return Response({"message": "can't find data"})
    

@rate_limiter
@api_view(['GET'])
def get_movie_data_with_rating(request, format='json'):
    if request.method == 'GET':
        feature = request.GET.get('feature')
        start_year = request.GET.get('start_year')
        end_year = request.GET.get('end_year')
        sort = request.GET.get('sort')
        if sort:
            pass
        else:
            sort = "rating_total_amount"
        imdb_rating = request.GET.get('imdb_rating')
        douban_rating = request.GET.get('douban_rating')
        start_num = int(request.GET.get('start', 0))
        movie_info = LatestRating.objects.select_related("internal").order_by(
            sort).reverse()
        if feature:
            id_result = FeatureMovieTable.objects.values("internal_id").filter(
                feature_id=feature)
            result = movie_info.filter(internal_id__in=id_result)
        else:
            result = movie_info
        if start_year:
            result = result.filter(
                    internal__start_year__gte=start_year).filter(
                    internal__start_year__lte=end_year)
        if imdb_rating:
            result = result.filter(imdb_rating__gte=imdb_rating)
        if douban_rating:
            result = result.filter(douban_rating__gte=douban_rating)
        count = result.count()
        print(count)
        serializer = LastestInfoSerializer(result[start_num:min(start_num + 20, count)], many=True)

        return Response(serializer.data)


@rate_limiter
@api_view(['GET'])
def search_movie(request, format=None):
    if request.method == 'GET':
        query = request.GET.get('query')
        movie_info = LatestRating.objects.select_related("internal")
        id_result = MovieOtherNames.objects.values("internal_id").filter(
            movie_name__icontains=query).distinct()
        result = movie_info.filter(internal_id__in=id_result).order_by(
            "internal__start_year").reverse()
        serializer = LastestInfoSerializer(result, many=True)
        return Response(serializer.data)


@rate_limiter
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_member_rating_movie(request, user_id, format=None):
    if request.method == 'GET':
        current_user_id = user_id
        movie_info = InternalUserRating.objects.select_related("internal")
        result = movie_info.filter(
            user_id=current_user_id).order_by("update_date").reverse()
        serializer = InternalUserRatingSerializer(result, many=True)
        return Response(serializer.data)


@rate_limiter
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_member_viewed_movie(request, user_id, format=None):
    if request.method == 'GET':
        current_user_id = user_id
        movie_info = MemberViewedRecord.objects.select_related("internal")
        result = movie_info.filter(
            user_id=current_user_id).order_by("viewed_date").reverse()
        serializer = MemberViewedRecordSerializer(result, many=True)
        return Response(serializer.data)


@rate_limiter
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_member_similarity(request, user_id, format=None):
    if request.method == 'GET':
        def nor(_list, mean_value, standard_dv):
            nor_result = []
            for i in _list:
                new_value = round((i - mean_value) / standard_dv, 3)
                nor_result.append(new_value)
            return nor_result
        
        def cosine_similarity(vec_a, vec_b):
            dot = sum(a * b for a, b in zip(vec_a, vec_b))
            norm_a = sum(a * a for a in vec_a)**0.5
            norm_b = sum(b * b for b in vec_b)**0.5
            cos_sim = dot / (norm_a * norm_b)
            return cos_sim
        current_user_id = user_id
        r = time.time()
        result = InternalUserRating.objects.filter(user_id=current_user_id)
        if len(result) < 10 :
            return JsonResponse({"message":"not enough"})
        internal_id = []
        internal_rating_dict = {}
        for i in result:
            internal_id.append(i.internal_id)
            internal_rating_dict[i.internal_id] = i.rating

        lastest_rating = LatestRating.objects.filter(internal_id__in=internal_id).filter(audience_rating__gt=0).filter(tomator_rating__gt=0)
        imdb_rating = []
        douban_rating = []
        audience_rating = []
        valid_internal_id_list= []
        for i in lastest_rating :
            valid_internal_id_list.append(i.internal_id)
            imdb_rating.append(float(i.imdb_rating))
            douban_rating.append(float(i.douban_rating))
            audience_rating.append(float(i.audience_rating)/10)

        valid_rating_list = []
        for i in valid_internal_id_list :
            valid_rating_list.append(internal_rating_dict[i])

        douban_stdev = 0.96684
        douban_mean = 6.8653
        imdb_stdev = 0.8288
        imdb_mean = 6.4562
        audience_stdev = 1.8659
        audience_mean = 5.9953
        douban_nor = nor(douban_rating, douban_mean, douban_stdev)
        imdb_nor = nor(imdb_rating, imdb_mean, imdb_stdev)
        audience_nor = nor (audience_rating,audience_mean,audience_stdev)
        internal_nor = valid_rating_list
        douban_internal = cosine_similarity(douban_nor, internal_nor)
        imdb_internal = cosine_similarity(imdb_nor, internal_nor)
        audience_internal = cosine_similarity(audience_nor,internal_nor)

        response_json = {}
        response_json['message'] = "successful"
        response_json["imdb"] = imdb_internal
        response_json["douban"] = douban_internal
        response_json["tomato"] = audience_internal

        return Response(response_json)


@rate_limiter
@api_view(['GET'])
def get_recommend_movies(request):
    if request.method == 'GET':
        feature = request.GET.get('feature')
        internal_id = request.GET.get('id')    
        
        if redis.get("feature_dict") :
            feature_dict =json.loads(redis.get("feature_dict"))
            for i in feature_dict :
                feature_dict[i] = set(feature_dict[i])
            print("redis")
            # print(feature_dict['3'])
        else :
            feature_dict = defaultdict(set)
            id_result = FeatureMovieTable.objects.all()
            for i in id_result:
                feature_dict[str(i.feature_id)].add(i.internal_id)
            redis_store_dict = {}
            for i in feature_dict :
                redis_store_dict[i] = list(feature_dict[i])
            redis.set('feature_dict',json.dumps(redis_store_dict), ex=300)
        if feature:
            feature_list = json.loads(feature)
            for i in range(len(feature_list)):
                if i == 0:
                    result = feature_dict[str(feature_list[i])]
                else:
                    result = result.intersection(feature_dict[str(feature_list[i])])
                    if len(result) <= 10 :
                        for insert_data in list(feature_dict[str(feature_list[i-1])]) :
                            result.add(insert_data)

        id_result = list(result)
        id_result.remove(int(internal_id))
        id_result = id_result[:min(50, len(id_result))]
        movie_info = LatestRating.objects.select_related("internal").order_by("imdb_rating", "rating_total_amount").reverse()
        recommend_result = movie_info.filter(internal_id__in=id_result)

        serializer = LastestInfoSerializer(recommend_result, many=True)
        return Response(serializer.data)


## Feature

@login_required
def score_movie(request):
    current_user = request.user
    get_dict = json.load(request)
    rating = get_dict['rating']
    internal_id = get_dict['internal_id']
    if request.method == "POST":
        try:
            review = InternalUserRating.objects.get(user_id=current_user.id,
                                                    internal_id=internal_id)
            review.rating = rating
            review.update_date = datetime.now()
        except:
            review = InternalUserRating(internal_id=internal_id,
                                        update_date=datetime.now(),
                                        rating=rating,
                                        user_id=current_user.id)
        review.save()
        return JsonResponse({"message": "success"})
    elif request.method == "DELETE":
        review = InternalUserRating.objects.get(user_id=current_user.id,
                                                internal_id=internal_id)
        review.delete()
        return JsonResponse({"message": "delete success"})
    # print(review_record)
    else:
        return JsonResponse({"message": "error"})


def logout(request):
    auth.logout(request)
    return redirect('/')


def report_error(request):
    if request.method == 'POST':
        current_user = request.user
        get_dict = json.load(request)
        internal_id = get_dict['internal_id']
        error_feature = get_dict['error_feature']
        error_msg = get_dict['error_msg']
        # review_record = InternalUserRating.objects.filter(user_id = current_user.id, movie_id= imdb_id)
        # if review_record.exists():
        if request.method == "POST":
            review = ErrorMsgRecord(internal_id=internal_id,
                                    user_id=current_user.id,
                                    update_date=datetime.now(),
                                    error_feature=error_feature,
                                    error_message=error_msg)
            review.save()
            return JsonResponse({"message": "success"})
