from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', views.home, name='home'),
    path('lines/create/', views.LineCreate.as_view(), name='line_create'),
    path('lines/<int:line_id>/', views.lines_detail, name='detail'),
    path('lines/<int:pk>/update/', views.LineUpdate.as_view(), name='line_update'),
    path('lines/<int:pk>/delete/', views.LineDelete.as_view(), name='line_delete'),
    path('accounts/signup/', views.signup, name='signup'),
    path('about/', views.about, name='about'),
    path('all/', views.all_lines, name='all_lines'),
    path('lines/<int:line_id>/add_wait/', views.add_wait, name='add_wait'),
    path('yelp/<str:yelp_id>/add_wait/', views.add_yelp_wait, name='add_yelp_wait'),
    path('waits/<int:wait_id>/<int:line_id>/', views.waits_detail, name='wait_detail'),
    path('waits/<int:pk>/update/', views.WaitUpdate.as_view(), name='wait_update'),
    path('waits/<int:wait_id>/delete/', views.WaitDelete, name='wait_delete'),
    path('search/', views.SearchResults, name='search_results'),
    path('lines/<int:line_id>/add_photo/', views.add_photo, name='add_photo'),
    path('yelp/<str:yelp_id>/', views.yelp_detail, name='yelp_detail'),
  	 path('favicon.ico', RedirectView.as_view(
  	     url=staticfiles_storage.url('images/favicon.ico'))),
]
