from django.conf.urls import url, include
from django.urls import path
from . import views

urlpatterns = [
    url(r'^api/movie/$', views.get_movie_data_with_rating),
    url(r'^api/movie/recommend$', views.get_recommend_movies),
    url(r"^api/detail/(?P<internal_id>\d+)/$", views.get_movie_detail_info),
    url(r"^api/search/$", views.search_movie),
    url(r"^api/member/(?P<user_id>\d+)/movies/$", views.get_member_rating_movie),
    url(r"^api/member/(?P<user_id>\d+)/similarity/$", views.get_member_similarity),
    url(r"^api/member/(?P<user_id>\d+)/viewed_movie/$", views.get_member_viewed_movie),
    url(r"^api/rating_status/$",views.get_update_rating_status_data),
    url(r"^api/movie_status/$",views.get_update_movie_status_data),
    
    path('', views.main_page, name='index'),
    path("movie/<internal_id>",views.movie_single_page),
    path("signup",views.sign_up),
    path("signin",views.sign_in),
    path("rating",views.score_movie),
    path("logout",views.logout),
    path("memberpage",views.member_page),
    path("search",views.advanced_search_page),
    path("basicSearch",views.search_by_word_page),
    path("report_error",views.report_error),
    path("dashboard",views.dashboard_page)
]