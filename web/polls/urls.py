from django.urls import path

from . import views

urlpatterns = [
    path('', views.main_page),
    path('test', views.index, name='index'),
    path("api/1.0/movies", views.get_movies_rating, name="movies")
]