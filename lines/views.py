from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from .models import *
from .services import get_yelp
import os
import json
# Define the home view


def home(request):
    return render(request, 'home.html', {'yelp': get_yelp()})


class LineCreate(LoginRequiredMixin, CreateView):
    model = Line
    fields = ['name', 'address', 'city', 'state',
              'postal_code', 'line_type', 'category', 'description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def lines_detail(request, line_id):
    line = Line.objects.get(id=line_id)
    photo = line.photo_set.all()
    wait = Wait.objects.filter(line=line_id)
    total = 0
    if len(wait) > 0:
        for w in wait:
            total += w.wait_time
        avg = total / len(wait)
        avg = round(avg, 1)
    else:
        avg = "No wait times submitted!"
    return render(request, 'lines/line_detail.html', {'line': line, 'photo': photo, 'avg':avg})


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


class WaitCreate(LoginRequiredMixin, CreateView):
    model = Wait
    fields = ['wait_time', 'party_size']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class WaitUpdate(UpdateView):
    model = Wait
    fields = ['wait_time', 'party_size']


class WaitDelete(DeleteView):
    model = Wait
    success_url = '/'


def waits_detail(request, wait_id, line_id):
    template_name = 'lines/wait_detail.html'
    wait = Wait.objects.filter(line=line_id)
    total = 0
    for w in wait:
      total += w.wait_time
    avg = total / len(wait)
    avg = round(avg,1)
    return render(request, 'lines/wait_detail.html', {'wait': wait, 'avg': avg})

class LineUpdate(UpdateView):
    model = Line
    fields = ['address', 'city', 'state',
              'postal_code', 'line_type', 'category', 'description']

class LineDelete(DeleteView):
  model = Line
  success_url = '/'

class SearchResultsView(ListView):
  model = Line
  template_name = 'search_results.html'

  def get_queryset(self):
    query = self.request.GET.get('q')
    locale = self.request.GET.get('l')
    queryset = Line.objects.filter(
        Q(name__icontains=query) | Q(line_type__icontains=query) | Q(category__icontains=query),
        Q(city__icontains=locale) | Q(state__icontains=locale) | Q(postal_code__icontains=locale)
      )
    return queryset
    

