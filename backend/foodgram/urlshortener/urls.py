from django.urls import path

from . import views


app_name = 'urlshortener'

urlpatterns = [
    path('s/<str:url_hash>/', views.url_load, name='url_load')
]
