
from django.urls import re_path, path
from . import views

urlpatterns = [
    # re_path(r"^(?P<username>\w+)/$", views.lobby),
    # re_path(r"^(?P<username>\w+)/$", views.lobby),
    # re_path(r'^chat/(?P<group>\w+)/(?P<username>\w+)/$', views.lobby),
    path('chat/<str:group>/', views.lobby),
]
