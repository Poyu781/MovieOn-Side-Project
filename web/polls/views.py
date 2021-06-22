from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.http import HttpResponse
# from .models import DoubanDetail,LatestRating,InternalUserRating
from django.db import transaction
from rest_framework import viewsets
from rest_framework import generics
from .serializers import MovieBasicSerializer,LastestInfoSerializer,InternalUserRatingSerializer,MemberViewedRecordSerializer
from .models import MovieBasicInfo,LatestRating,FeatureMovieTable,FeatureTable,InternalUserRating,MovieOtherNames,InternalUserRating,MemberViewedRecord
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
import time
from statistics import mean, pstdev
from collections import defaultdict
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# @api_view(['GET'])
# def test(request,format=None):
    # cursor= connection.cursor()
    # cursor.execute('')
    # result = dictfetchall(cursor)
    # # print(type(result))
    # # # r = {"test":12}
    # # # result[0].update(r)
    # print(result)
    # return Response(result)
@api_view(['GET'])
def show_detail(request,internal_id,format=None,):
    print(internal_id)
    cursor= connection.cursor()
    cursor.execute(f"CALL `get_movie_detail_procedure`({int(internal_id)})")
    result = dictfetchall(cursor)
    cursor.execute(f"CALL `get_director_actor_feature`({int(internal_id)})")
    result[0].update(dictfetchall(cursor)[0])
    return Response(result)

@api_view(['GET'])
def get_movie_data_with_rating(request, format=None):
    if request.method == 'GET':
        feature = request.GET.get('feature')
        start_year = request.GET.get('start_year')
        end_year = request.GET.get('end_year')
        sort = request.GET.get('sort')
        if sort:
            pass
        else :
            sort = "rating_total_amount"
        imdb_rating = request.GET.get('imdb_rating')
        douban_rating = request.GET.get('douban_rating')
        start_num = int(request.GET.get('start',0))
        movie_info = LatestRating.objects.select_related("internal").order_by(sort).reverse()
        if feature :
            # if feature.count(","):
            id_result = FeatureMovieTable.objects.values("internal_id").filter(feature_id=feature)
            # print(id_result)
            result = movie_info.filter(internal_id__in =id_result)
        else:
            result = movie_info
        if start_year :
            result = result.filter(internal__start_year__gte=start_year).filter(internal__start_year__lte=end_year)
        if imdb_rating :
            result = result.filter(imdb_rating__gte=imdb_rating)
        if douban_rating :
            result = result.filter(douban_rating__gte=douban_rating)
        count = result.count()
        # print(start_num)
        print(count)
        serializer = LastestInfoSerializer(result[start_num:min(start_num+20,count)], many=True)
        # print(type(serializer.data))
        # print(serializer)
        return Response(serializer.data)

@api_view(['GET'])
def search_movie(request, format=None):
    if request.method == 'GET':
        query = request.GET.get('query')

        movie_info = LatestRating.objects.select_related("internal")
        id_result = MovieOtherNames.objects.values("internal_id").filter(movie_name__icontains=query).distinct()
        # print(id_result)
        result = movie_info.filter(internal_id__in =id_result).order_by("internal__start_year").reverse()
        # print(id_result)
        # print(count)
        serializer = LastestInfoSerializer(result, many=True)
        # print(type(serializer.data))
        # print(serializer)
        return Response(serializer.data)


@api_view(['GET'])
def get_member_reviewed_movie(request,user_id, format=None):
    if request.method == 'GET':
        current_user_id = user_id
        movie_info = InternalUserRating.objects.select_related("internal")
        result = movie_info.filter(user_id =current_user_id).order_by("update_date").reverse()
        serializer = InternalUserRatingSerializer(result, many=True)
        # print(type(serializer.data))
        # print(serializer)
        return Response(serializer.data)

@api_view(['GET'])
def get_member_viewed_movie(request,user_id, format=None):
    if request.method == 'GET':
        current_user_id = user_id
        movie_info = MemberViewedRecord.objects.select_related("internal")
        result = movie_info.filter(user_id =current_user_id).order_by("viewed_date").reverse()
        serializer = MemberViewedRecordSerializer(result, many=True)
        # print(type(serializer.data))
        # print(serializer)
        return Response(serializer.data)


@api_view(['GET'])
def get_member_similarity(request,user_id, format=None):
    if request.method == 'GET':
        current_user_id = user_id
        r = time.time()
        movie_info = InternalUserRating.objects.select_related("internal")

        result = movie_info.filter(user_id =current_user_id).order_by("internal_id")
        internal_id = []
        internal_rating = []
        
        for i in result:
            internal_id.append(i.internal.internal_id)
            internal_rating.append(i.rating)
        internal_stdev = pstdev(internal_rating)
        internal_mean = mean(internal_rating)

        lastest_rating = LatestRating.objects.filter(internal_id__in=internal_id)
        imdb_rating  = []
        douban_rating = []
        audience_rating = []
        
        for i in lastest_rating:
            print(i.internal_id)
            imdb_rating.append(float(i.imdb_rating))
            douban_rating.append(float(i.douban_rating))
            # audience_rating.append(float(i.audience_rating)/10)
        print(internal_id)
        def nor(_list,mean_value,standard_dv):
            nor_result =[]
            for i in _list:
                new_value = round((i - mean_value) / standard_dv,3)
                nor_result.append(new_value)
            return nor_result
        douban_stdev = 0.96684
        douban_mean = 6.8653
        imdb_stdev = 0.8288
        imdb_mean = 6.4562
        audience_stdev = 1.8659
        audience_mean = 5.9953
        douban_nor = nor(douban_rating,douban_mean,douban_stdev)
        imdb_nor = nor(imdb_rating,imdb_mean,imdb_stdev)
        # audience_nor = nor (audience_rating,audience_mean,audience_stdev)
        internal_nor = nor(internal_rating,internal_mean,internal_stdev)
        def cosine_similarity(vec_a,vec_b):
            dot = sum(a*b for a, b in zip(vec_a, vec_b))
            norm_a = sum(a*a for a in vec_a) ** 0.5
            norm_b = sum(b*b for b in vec_b) ** 0.5
            cos_sim = dot / (norm_a*norm_b)
            return cos_sim
        douban_internal = cosine_similarity(douban_nor,internal_nor)
        imdb_internal = cosine_similarity(imdb_nor,internal_nor)
        # audience_internal = cosine_similarity(audience_nor,internal_nor)
        print(douban_nor,imdb_nor,internal_nor)
        # rate = result.values("internal__internal")
        print("time",time.time()-r)
        # print(id_result)
        # print(count)
        response_json = {}
        response_json["imdb"] = imdb_internal
        response_json["douban"] = douban_internal
        # response_json["tomato"] = audience_internal
        # print(type(serializer.data))
        # print(serializer)
        return Response([response_json])    


feature_dict = defaultdict(set)
@api_view(['GET'])
def get_recommend_movies(request):
    feature = request.GET.get('feature')
    internal_id = request.GET.get('id')
    start  = time.time()
    if feature_dict :
        pass
    else:
        id_result = FeatureMovieTable.objects.all()
        for i in id_result:
            feature_dict[i.feature_id].add(i.internal_id)
    if feature:
        feature_list = json.loads(feature)
        for i in range(len(feature_list)) :
            if i == 0:
                result = feature_dict[feature_list[i]]
            else:
                result = result.intersection(feature_dict[feature_list[i]])

    id_result = list(result)
    id_result.remove(int(internal_id))
    movie_info = LatestRating.objects.select_related("internal").order_by("imdb_rating","rating_total_amount").reverse()
    recommend_result = movie_info.filter(internal_id__in =id_result)
    print(time.time()-start)
    serializer = LastestInfoSerializer(recommend_result[:min(50,len(id_result))], many=True)
    return Response(serializer.data)
def advanced_search_page(request):
    
    return render(request,"advanced_search_page.html")

def search_by_word_page(request):
    
    return render(request,"search_by_word_page.html")


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
    if str(request.user) != "AnonymousUser":
        current_user = request.user
        try:
            review = MemberViewedRecord.objects.get(user_id = current_user.id, internal_id= internal_id)
            review.viewed_date = datetime.now()
        except:
            review = MemberViewedRecord(internal_id = internal_id, viewed_date	 = datetime.now(), user_id = current_user.id)
        review.save()
    
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
    internal_id = get_dict['internal_id']
        # review_record = InternalUserRating.objects.filter(user_id = current_user.id, movie_id= imdb_id)
        # if review_record.exists():
    if request.method == "POST":
        try:
            review = InternalUserRating.objects.get(user_id = current_user.id, internal_id= internal_id)
            review.rating = rating
            review.update_date = datetime.now()
        except:
            review = InternalUserRating(internal_id = internal_id, update_date = datetime.now(), rating = rating, user_id = current_user.id)
        review.save()
    elif request.method == "DELETE":
        review = InternalUserRating.objects.get(user_id = current_user.id, internal_id= internal_id)
        review.delete()
        return JsonResponse({"message":"delete success"})
    # print(review_record)
    else :
        return JsonResponse({"message":"error"})

    return JsonResponse({"message":"success"})


def logout(request):
    auth.logout(request)
    return redirect('/')