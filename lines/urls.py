from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('lines/create/', views.LineCreate.as_view(), name='line_create'),
    path('lines/<int:line_id>/', views.lines_detail, name='detail'),
]
