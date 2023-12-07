from django.urls import path
from . import views

app_name = "chatgroup"
urlpatterns = [
    path('', views.index, name='homechat'),
    path('<str:room_name>/', views.room, name='room'),
]