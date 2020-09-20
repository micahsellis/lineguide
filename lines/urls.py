from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('lines/create/', views.LineCreate.as_view(), name='line_create'),
    path('lines/<int:line_id>/', views.lines_detail, name='detail'),
    path('lines/<int:pk>/update/', views.LineUpdate.as_view(), name='line_update'),
    path('lines/<int:pk>/delete/', views.LineDelete.as_view(), name='line_delete'),
    path('accounts/signup/', views.signup, name='signup'),
    path('about/', views.about, name='about'),
    path('all/', views.all_lines, name='all_lines'),
    path('waits/create/', views.WaitCreate.as_view(), name='wait_create'),
    path('waits/<int:wait_id>/', views.waits_detail, name='wait_detail'),
    path('waits/<int:pk>/update/', views.WaitUpdate.as_view(), name='wait_update'),
    path('waits/<int:pk>/delete/', views.WaitDelete.as_view(), name='wait_delete'),
]
