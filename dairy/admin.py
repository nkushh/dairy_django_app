from django.contrib import admin
from .models import Cow, Milk, MilkSale

# Register your models here.
admin.site.register(Cow)
admin.site.register(Milk)
admin.site.register(MilkSale)