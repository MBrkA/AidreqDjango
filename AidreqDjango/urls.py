"""
URL configuration for AidreqDjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, re_path
from front import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main),
    path('home/', views.home),
    path('logout/', views.logout),
    ## FORM PAGES
    path('search_item/', views.search_item),
    path('get_all_items/', views.get_all_items),
    path('update_item/', views.update_item),
    path('delete_item/', views.delete_item),
    path('create_campaign/', views.create_campaign),
    path('add_request/', views.add_request),
    path('get_request/', views.get_request),
    path('update_request/', views.update_request),
    path('remove_request/', views.remove_request),
    path('query/', views.query),
    path('watch/', views.watch),
    path('unwatch/', views.unwatch),
    path('mark_available/', views.mark_available),
    path('pick/', views.pick),
    path('arrived/', views.arrived),
    ## API
    re_path('login_post/', views.login_post),
    re_path('search_item_post/', views.search_item_post),
    re_path('get_all_items_post/', views.get_all_items_post),
    re_path('update_item_post/', views.update_item_post),
    re_path('delete_item_post/', views.delete_item_post),
    re_path('create_campaign_post/', views.create_campaign_post),
    re_path('add_request_post/', views.add_request_post),
    re_path('get_request_post/', views.get_request_post),
    re_path('update_request_post/', views.update_request_post),
    re_path('remove_request_post/', views.remove_request_post),
    re_path('query_post/', views.query_post),
    re_path('watch_post/', views.watch_post),
    re_path('unwatch_post/', views.unwatch_post),
    re_path('mark_available_post/', views.mark_available_post),
    re_path('pick_post/', views.pick_post),
    re_path('arrived_post/', views.arrived_post),


]