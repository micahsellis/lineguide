from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Line(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    postal_code = models.CharField(max_length=10, blank=True)
    line_type = models.CharField(max_length=100)
    category = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=500, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'line_id': self.id})

class Yelp(models.Model):
    business_id = models.CharField(max_length=100)

class Photo(models.Model):
    url = models.CharField(max_length=200)
    line = models.ForeignKey(Line, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for line_id: {self.line_id} @{self.url}"

class Wait(models.Model):
    wait_time = models.IntegerField()
    party_size = models.IntegerField()
    business_id = models.CharField(max_length=100)
    line = models.ForeignKey(Line, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('all_lines', kwargs={'pk': self.id})
