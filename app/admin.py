from django.contrib import admin
from .models import Chickens, ChickenHistory

@admin.register(Chickens)

class ChickensAdmin(admin.ModelAdmin):
    list_display = ['tag_number', 'fowl_pox_vaccine', 'birthdate', 'is_infected']
    list_filter = ['fowl_pox_vaccine', 'is_infected']
    search_fields = ['tag_number']


@admin.register(ChickenHistory)
class ChickenHistoryAdmin(admin.ModelAdmin):
    list_display = ['chicken', 'is_morning_bath', 'is_afternoon_bath', 'is_vitamin_a', 'is_vitamin_d',
                    'is_vitamin_e', 'is_vitamin_k', 'is_vitamin_b1', 'date']
    list_filter = ['is_morning_bath', 'is_afternoon_bath', 'is_vitamin_a', 'is_vitamin_d',
                   'is_vitamin_e', 'is_vitamin_k', 'is_vitamin_b1', 'date']
    search_fields = ['chicken__tag_number'] 