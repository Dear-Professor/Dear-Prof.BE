from django.contrib import admin
from .models import *

admin.site.register(SentEmail)
admin.site.register(ReceivedEmail)