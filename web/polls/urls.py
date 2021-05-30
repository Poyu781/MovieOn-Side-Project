from django.conf.urls import url, include
from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register('movie_detail',views.DoubanDetailView)
# router.register('rating',views.LatestRatingView)
router.register('basic',views.MovieBasicView)
router.register('rating',views.LastestRatingView)
urlpatterns = [
    url(r'^api/', include(router.urls)),
    path('', views.main_page, name='index'),
    # path('test',views.index),
    # path("movie/<imdb_id>",views.movie_single_page),
    path("signup",views.sign_up),
    path("signin",views.sign_in),
    # path("rating",views.score_movie),
    path("logout",views.logout),
    path("memberpage",views.member_page),
    path("test",views.test),
    path("xo",views.MoviesView.as_view())

    # path("api/1.0/movies", views.get_movies_rating, name="movies"),
    # path("api/1.0/douban_detail",views.DoubanDetailView.as_view())
]
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    url(r'^snippets/$', views.snippet_list),
]

urlpatterns = format_suffix_patterns(urlpatterns)