from django.urls import path, include
from faceregister import views


urlpatterns = [
    path('', views.index, name='index'),
    ]
