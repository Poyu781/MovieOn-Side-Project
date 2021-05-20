from django.conf.urls import url, include
from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('Do',views.DoubanDetailView)
router.register('rating',views.LatestRatingView)
urlpatterns = [
    url(r'^api/', include(router.urls)),
    path('', views.main_page, name='index'),
    path('test',views.index)
    # path("api/1.0/movies", views.get_movies_rating, name="movies"),
    # path("api/1.0/douban_detail",views.DoubanDetailView.as_view())
]