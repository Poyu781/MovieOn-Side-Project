from django.conf.urls import url, include
from django.urls import path
from . import views

urlpatterns = [
    url(r'^api/movie/$', views.get_home_page_data),
    url(r"^api/detail/(?P<internal_id>\d+)/$", views.show_detail),
    url(r"^api/test/$", views.test),
    url(r"^api/search/$", views.search_movie),
    path('', views.main_page, name='index'),
    path("movie/<internal_id>",views.movie_single_page),
    path("signup",views.sign_up),
    path("signin",views.sign_in),
    path("rating",views.score_movie),
    path("logout",views.logout),
    path("memberpage",views.member_page),

    # path("api/1.0/movies", views.get_movies_rating, name="movies"),
    # path("api/1.0/douban_detail",views.DoubanDetailView.as_view())
]