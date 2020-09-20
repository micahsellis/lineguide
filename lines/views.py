from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
# Add the following import
from django.http import HttpResponse
from .models import *
from .services import get_yelp
import os
# Define the home view


def home(request):
  return render(request, 'home.html', {'yelp':get_yelp()})

class LineCreate(CreateView):
    model = Line
    fields = ['name', 'address', 'city', 'state', 'postal_code', 'line_type', 'category']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

def lines_detail(request, line_id):
    line = Line.objects.get(id=line_id)
    return render(request, 'lines/detail.html', {'line': line})
    

def some_function(request):
    my_key = os.environ['API_KEY']
    client_id = os.environ['CLIENT_ID']
   
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
