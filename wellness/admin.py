from django.contrib import admin
from .models import StressTrigger, WellnessLog

admin.site.register(StressTrigger)
admin.site.register(WellnessLog)