from django.urls import path, include
from .views import Request_all, Create_user, Request_create, Request_update,Request_delete

urlpatterns = [
    path('', include('allauth.urls')),
    path('create_user', Create_user.as_view(), name='signup'),
    path('', Request_all.as_view(), name='request'),
    path('request_create', Request_create.as_view(), name='request_create'),
    path('request_update/<int:pk>', Request_update.as_view(), name='request_update'),
    path('request_delete/<int:pk>', Request_delete.as_view(), name='request_delete')
]
