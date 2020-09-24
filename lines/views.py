from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from .forms import WaitForm
from .models import *
from .services import get_yelp
import os
import json
import uuid
import boto3
# Define the home view

S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'lineguide-me'

def home(request):
    return render(request, 'home.html', {'yelp': get_yelp()})


class LineCreate(LoginRequiredMixin, CreateView):
    model = Line
    fields = ['name', 'address', 'city', 'state',
              'postal_code', 'line_type', 'category', 'description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def add_photo(request, line_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      Photo.objects.create(url=url, line_id=line_id)
    except:
      print('An error occured uploading file to S3')
  return redirect('detail', line_id=line_id)

def lines_detail(request, line_id):
    line = Line.objects.get(id=line_id)
    photo = line.photo_set.all()
    wait_form = WaitForm()
    wait = Wait.objects.filter(line=line_id)
    total = 0
    if len(wait) > 0:
        for w in wait:
            total += w.wait_time
        avg = total / len(wait)
        avg = round(avg, 1)
    else:
        avg = 0
    return render(request, 'lines/line_detail.html', {'line': line, 'photo': photo, 'avg':avg, 'wait_form': wait_form})


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


def about(request):
    return render(request, 'about.html')


def all_lines(request):
    lines = Line.objects.filter(user=request.user.id)
    return render(request, 'lines/all.html', {'lines': lines})


def add_wait(request, line_id):
    form = WaitForm(request.POST)
    if form.is_valid():
        new_wait = form.save(commit=False)
        new_wait.user_id = request.user.id
        new_wait.line_id = line_id
        new_wait.save()
    return redirect('detail', line_id=line_id)

class WaitUpdate(LoginRequiredMixin, UpdateView):
    model = Wait
    fields = ['wait_time', 'party_size']

    def form_valid(self, form):
        if form.instance.user == self.request.user:
            return super().form_valid(form)
        else:
            return redirect('/')


class WaitDelete(LoginRequiredMixin, DeleteView):
    model = Wait
    success_url = '/'

    def form_valid(self, form):
        if form.instance.user == self.request.user:
            return super().form_valid(form)
        else:
            return redirect('/')

def waits_detail(request, wait_id, line_id):
    template_name = 'lines/wait_detail.html'
    wait = Wait.objects.filter(line=line_id)
    total = 0
    for w in wait:
      total += w.wait_time
    avg = total / len(wait)
    avg = round(avg,1)
    return render(request, 'lines/wait_detail.html', {'wait': wait, 'avg': avg})

class LineUpdate(LoginRequiredMixin, UpdateView):
    model = Line
    fields = ['address', 'city', 'state',
              'postal_code', 'line_type', 'category', 'description']

    def form_valid(self, form):
        if form.instance.user == self.request.user:
            return super().form_valid(form)
        else:
            return redirect('/')



class LineDelete(LoginRequiredMixin, DeleteView):
  model = Line
  success_url = '/'

  def form_valid(self, form):
        if form.instance.user == self.request.user:
            return super().form_valid(form)
        else:
            return redirect('/')

class SearchResultsView(ListView):
  model = Line
  template_name = 'search_results.html'

  def get_queryset(self):
    query = self.request.GET.get('q')
    locale = self.request.GET.get('l')
    # cat = self.request.GET.get('c')
    queryset = Line.objects.filter(
        Q(name__icontains=query) | Q(line_type__icontains=query) | Q(category__icontains=query),
        Q(city__icontains=locale) | Q(state__icontains=locale) | Q(postal_code__icontains=locale)#,
        # Q(line_type__icontains=cat)
      )
    return queryset
    

