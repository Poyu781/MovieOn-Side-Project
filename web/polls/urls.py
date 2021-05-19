from django.urls import path

from . import views

urlpatterns = [
    path('', views.hello_word),
    path('test', views.index, name='index')
    # path("api/1.0/"), views.get
]