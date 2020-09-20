from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from .models import *
from .services import get_yelp
import os
# Define the home view


def home(request):
  return render(request, 'home.html', {'yelp':get_yelp()})


class LineCreate(LoginRequiredMixin, CreateView):
    model = Line
    fields = ['name', 'address', 'city', 'state', 'postal_code', 'line_type', 'category']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

def lines_detail(request, line_id):
    line = Line.objects.get(id=line_id)
    return render(request, 'lines/detail.html', {'line': line})
   
def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def about(request):
  return render(request, 'about.html')

def all_lines(request):
    lines = Line.objects.all()
    return render(request, 'lines/all.html', {'lines': lines})