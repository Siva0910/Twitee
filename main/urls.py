from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('logout/', views.logout1, name='logout'),
    path('create-post/', views.create_post, name='create_post'),
    path('my-post/',views.my_post, name='my_post'),
]