"""tweetanalysis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from userapp import views as userapp_views
from mainapp import views as mainapp_views
from adminapp import views as adminapp_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',mainapp_views.index,name='index'),

    #main
    path('about', mainapp_views.about,name='about'),
    
    
    #user
    path('user-register',userapp_views.user_register,name='user_register'),
    path('user-login',userapp_views.user_login,name='user_login'),
    path('user-logout',userapp_views.user_logout,name='user_logout'),
    path('user-dashboard',userapp_views.user_dashboard,name='user_dashboard'),
    path('user-search-result',userapp_views.user_search_result,name='user_search_result'),
    path('user-search-tweets.html',userapp_views.user_search_tweets,name='user_search_tweets'),
    path('user-profile',userapp_views.user_profile,name='user_profile'),
    path('user-twitter-profile',userapp_views.user_twitter_profile,name='user_twitter_profile'),
    path('user-search-result/<str:tagname>',userapp_views.trending_search,name='trending_search'),

    #admin
    path('admin-login',adminapp_views.admin_login,name='admin_login'),
    path('admin-logout',adminapp_views.admin_logut,name='admin_logout'),
    path('admin-dashboard',adminapp_views.admin_dashboard,name='admin_dashboard'),
    path('admin-searched-tweets-list',adminapp_views.admin_searched_tweets_list,name='admin_searched_tweets_list'),
    path('admin-view-users',adminapp_views.admin_view_users,name='admin_view_users'),
    path('admin_user_status/<int:user_id>/<str:status>',adminapp_views.admin_user_status,name='admin_user_status'),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
