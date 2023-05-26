from rest_framework import serializers
from .models import Chickens
from .models import ChickenHistory
from .models import Disease
from .models import Symptom

class ChickensSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chickens
        fields = ['id', 'tag_number', 'fowl_pox_vaccine', 'birthdate', 'is_infected', 'picture']



class ChickenHistorySerializerJoined(serializers.ModelSerializer):

    chicken_fowl_pox_vaccine = serializers.BooleanField(source='chicken.fowl_pox_vaccine')
    chicken_verdict = serializers.CharField(source='chicken.verdict')
    is_infected = serializers.CharField(source='chicken.is_infected')
    tag_number = serializers.CharField(source='chicken.tag_number')
    class Meta:
        model = ChickenHistory
        fields = '__all__'


class ChickenHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChickenHistory
        fields = '__all__'



class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = '__all__'


class SymptomsSerializer(serializers.ModelSerializer):
    disease_name = serializers.CharField(source='disease.name')
    class Meta:
        model = Symptom
        fields = '__all__'