from django.forms import ModelForm
from .models import Wait


class WaitForm(ModelForm):
  class Meta:
    model = Wait
    fields = ['wait_time', 'party_size']
