from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Agency)
admin.site.register(Destination)
admin.site.register(Transaction)
