from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Line)
admin.site.register(Wait)
admin.site.register(Photo)
admin.site.register(Yelp)


# admin.site.register(Hour)