from rest_framework import serializers
from .models import Chickens
from .models import ChickenHistory

class ChickensSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chickens
        fields = ['id', 'tag_number', 'fowl_pox_vaccine', 'birthdate', 'is_infected', 'picture']



class ChickenHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChickenHistory
        fields = ['id', 'chicken', 'is_morning_bath', 'is_afternoon_bath', 'is_vitamin_a',
                  'is_vitamin_d', 'is_vitamin_e', 'is_vitamin_k', 'is_vitamin_b1', 'date']