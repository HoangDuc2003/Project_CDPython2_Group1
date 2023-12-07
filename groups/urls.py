from chat.models import Room
from django.urls import path,re_path
from .views import GroupDeleteView

from .import views
app_name = 'groups'

urlpatterns =[
    re_path(r"^$", views.ListGroups, name="all"),
    re_path(r"^new/$", views.CreateGroup, name="create"),
    re_path(r"join/(?P<slug>[-\w]+)/$",views.JoinGroup.as_view(),name="join"),
    re_path(r"leave/(?P<slug>[-\w]+)/$",views.LeaveGroup.as_view(),name="leave"),
    path("delgr/<int:id>", GroupDeleteView, name="delgr"),
]