from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.http import HttpResponse
# from .models import DoubanDetail,LatestRating,InternalUserRating
from django.db import transaction
from rest_framework import viewsets
from rest_framework import generics
from .serializers import MovieBasicSerializer,LastestInfoSerializer,FeaSer
from .models import MovieBasicInfo,LatestRating,FeatureMovieTable,FeatureTable
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
from rest_framework.pagination import LimitOffsetPagination

@api_view(['GET'])
def snippet_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        feature = request.GET.get('feature')
        start_num = request.GET.get('start',0)
        print(start_num)
        id_result = FeatureMovieTable.objects.values("internal_id").filter(feature_id=feature)
        snippets = LatestRating.objects.select_related("internal").order_by("internal__start_year").reverse()
        count = snippets.count()
        print(count)
        result = snippets.filter(internal_id__in =id_result)[0:20]
        serializer = LastestInfoSerializer(result, many=True)
        # print(type(serializer.data))
        # print(serializer)
        return Response(serializer.data)
class MoviesView(generics.GenericAPIView):
    queryset = LatestRating.objects.all().select_related("internal")
    serializer_class = LastestInfoSerializer
    def get(self, request, *args, **krgs):
        users = self.get_queryset()[:10]
        serializer = self.serializer_class(users, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)
    # def post(self, request, *args, **krgs):
    #     data = request.data
    #     try:
    #         serializer = self.serializer_class(data=data)
    #         serializer.is_valid(raise_exception=True)
    #         with transaction.atomic():
    #             serializer.save()
    #         data = serializer.data
    #     except Exception as e:
    #         data = {'error': str(e)}
    #     return JsonResponse(data)
class MovieBasicView(viewsets.ModelViewSet):
    queryset = MovieBasicInfo.objects.all()
    serializer_class = MovieBasicSerializer
    # filter_backends = [DjangoFilterBackend]
    @action(methods=["get"],detail=False)
    def get(self, request, *args, **krgs):
        feature = request.GET.get('num')
        id_result = FeatureMovieTable.objects.values("internal_id").filter(feature_id=feature)
        fetch = self.get_queryset().filter(internal_id__in =id_result)
        print(fetch.query)
        serializer = self.serializer_class(fetch, many=True)
        data = serializer.data
        return Response(data)
    # brand = request.GET.get('brand')

    # if brand :
    #     id_result = FeatureMovieTable.objects.values("internal_id").filter(feature_id=3)
    # else :
    #     id_result = (1040,1041)
    # .filter(id__in=id_result)
    
class LastestRatingView(viewsets.ModelViewSet):
    queryset = LatestRating.objects.all()
    # queryset = LastestInfoSerializer.setup_eager_loading(queryset=queryset_a)
    serializer_class = LastestInfoSerializer
    @action(methods=["get"],detail=False)
    def feature(self, request, *args, **krgs):
        feature = request.GET.get('num')
        id_result = FeatureMovieTable.objects.values("internal_id").filter(feature_id=feature)
        fetch = self.get_queryset().filter(internal_id__in =id_result)
        print(fetch.query)
        serializer = self.serializer_class(fetch, many=True)
        data = serializer.data
        return Response(data)
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['internal_id']
# class DoubanDetailView(viewsets.ModelViewSet):
#     queryset = DoubanDetail.objects.all()
#     serializer_class = DoubanDetailSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['imdb_id']
# class LatestRatingView(viewsets.ModelViewSet):
#     queryset = LatestRating.objects.all().select_related('imdb')
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['imdb_id']
#     serializer_class = LatestRatingSerializer
from django.core.serializers import serialize
def test(request):
    result = LatestRating.objects.all().select_related("internal")[:5]#raw("SELECT * FROM latest_rating inner join movie_basic_info on latest_rating.internal_id = movie_basic_info.internal_id limit 1")
    print(serialize("json",result))
    for i in result :
        # print(serialize("json",i))
        print(i.internal.main_original_name)

    # data = serialize("json",result)
    # print(result.query)
    # r = {"data":data}
    # return JsonResponse(r)

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def main_page(request):
    # print(DoubanDetail.objects.filter(douban_id__contains="7916239")[0].movie_title)

    return render(request,"home_page.html")

@login_required
def member_page(request):
    return render(request,"member_page.html")

# @login_required
def movie_single_page(request,imdb_id):
    current_user = request.user
    data = DoubanDetail.objects.filter(imdb_id= imdb_id)
    content = list(data.values())[0]
    try :
        review = InternalUserRating.objects.get(user_id = current_user.id, movie_id= imdb_id)
        content['rating']=review.rating
    except:
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

# def test(request):
#     r = 
# class PttHomeView(GenericAPIView):
#     queryset = Ptt.objects.all().prefetch_related(“landtop”)
#     serializer_class = PttSerializer
#     def get(self, request, *args, **krgs):
#         start = time.time()
#         brand = request.GET.get(‘brand’)
#         phones = get_phones()
#         if brand:
#             fetch = (self.get_queryset()
#             .values(‘title’, ‘storage’, “landtop__price”)
#             .annotate(old_price=Round(Avg(‘price’, output_field=FloatField()), 0),
#                       id=Max(‘id’, output_field=IntegerField()),
#                       new_price=F(‘landtop__price’))
#             .filter(price__gte=1000, new=0, title__in=phones, title__startswith=brand, created_at__gte=datetime.now()-timedelta(days=30))
#             .exclude(storage__isnull=True, price__isnull=True)
#             .order_by(‘title’))
#         else:
#             fetch = (self.get_queryset()
#             .values(‘title’, ‘storage’, “landtop__price”)
#             .annotate(old_price=Round(Avg(‘price’, output_field=FloatField()), 0),
#                       id=Max(‘id’, output_field=IntegerField()),
#                       new_price=F(‘landtop__price’))
#             .filter(price__gte=1000, new=0, title__in=phones, created_at__gte=datetime.now()-timedelta(days=30))
#             .exclude(storage__isnull=True, price__isnull=True)
#             .order_by(‘title’))
#         print(fetch.query)
#         serializer = self.serializer_class(fetch, many=True)
#         data = serializer.data
#         print(time.time() - start)
#         return JsonResponse({“data”: data})
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
        review = InternalUserRating.objects.get(user_id = current_user.id, movie_id= imdb_id)
        print(review)
        review.rating = rating
        review.update_date = datetime.now()
    except:
        review = InternalUserRating(movie_id = imdb_id, update_date = datetime.now(), rating = rating, user_id = current_user.id)
        print(1)
    review.save()
    # print(review_record)

    return JsonResponse({"message":"success"})


def logout(request):
    auth.logout(request)
    return redirect('/')