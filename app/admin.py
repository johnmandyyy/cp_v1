from django.contrib import admin
from .models import Chickens

@admin.register(Chickens)
class ChickensAdmin(admin.ModelAdmin):
    list_display = ['tag_number', 'fowl_pox_vaccine', 'birthdate', 'is_infected']
    list_filter = ['fowl_pox_vaccine', 'is_infected']
    search_fields = ['tag_number']
