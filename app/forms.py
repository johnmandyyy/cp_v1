"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))



from django import forms
from .models import Chickens, ChickenHistory


from django.forms.widgets import DateInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from .models import Symptom
from .models import Disease
from .models import Predictions


class ChickensForm(forms.ModelForm):
    birthdate = forms.DateField(widget=DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'tag_number',
            'fowl_pox_vaccine',
            'is_infected',
            'birthdate',
            Submit('submit', 'Submit')
        )

    class Meta:
        model = Chickens
        fields = ['tag_number', 'fowl_pox_vaccine', 'is_infected', 'birthdate']

class ChickenHistoryForm(forms.ModelForm):
    class Meta:
        model = ChickenHistory
        fields = ['is_morning_bath', 'is_afternoon_bath', 'is_vitamin_a', 'is_vitamin_d',
                  'is_vitamin_e', 'is_vitamin_k', 'is_vitamin_b1']
        labels = {
            'is_morning_bath': 'Tapos na ba sa umagang pagligo?',
            'is_afternoon_bath': 'Tapos na ba hapon na pagligo?',
            'is_vitamin_a': 'Nakainom na ng Vitamin A?',
            'is_vitamin_d': 'Nakainom na ng Vitamin D?',
            'is_vitamin_e': 'Nakainom na ng Vitamin E?',
            'is_vitamin_k': 'Nakainom na ng Vitamin K?',
            'is_vitamin_b1': 'Nakainom na ng Vitamin B1?',
        }


class DiseasesForm(forms.ModelForm):

    class Meta:
        from .models import Disease
        model = Disease
        fields = ['name']
        labels = {'name': 'Name of Disease'}
        
class SymptomsForm(forms.ModelForm):

    disease = forms.ModelChoiceField(label='Disease', queryset=Disease.objects.all())
    warts = forms.BooleanField(label='Warts')
    loss_of_appetite = forms.BooleanField(label='Loss of Appetite')
    lesions = forms.BooleanField(label='Lesions')
    blister = forms.BooleanField(label='Blister')
    swelling_eyes = forms.BooleanField(label='Swelling Eyes')
    weight_loss = forms.BooleanField(label='Weight Loss')
    reducted_water_consumption = forms.BooleanField(label='Reduced Water Consumption')
    diarrhea = forms.BooleanField(label='Diarrhea')
    less_egg_production = forms.BooleanField(label='Less Egg Production')
    difficulty_breathing = forms.BooleanField(label='Difficulty Breathing')
    pale_comb = forms.BooleanField(label='Pale Comb')
    nasal_discharge = forms.BooleanField(label='Nasal Discharge')
    watery_eyes = forms.BooleanField(label='Watery Eyes')
    paralysis = forms.BooleanField(label='Paralysis')
    watery_feces = forms.BooleanField(label='Watery Feces')

    class Meta:
        model = Symptom
        fields = ['disease', 'warts', 'loss_of_appetite', 'lesions', 'blister', 'swelling_eyes', 'weight_loss', 'reducted_water_consumption', 'diarrhea', 'less_egg_production', 'difficulty_breathing', 'pale_comb', 'nasal_discharge', 'watery_eyes', 'paralysis', 'watery_feces']


class PredictionSymptomsForm(forms.ModelForm):
    warts = forms.BooleanField(label='Warts')
    loss_of_appetite = forms.BooleanField(label='Loss of Appetite')
    lesions = forms.BooleanField(label='Lesions')
    blister = forms.BooleanField(label='Blister')
    swelling_eyes = forms.BooleanField(label='Swelling Eyes')
    weight_loss = forms.BooleanField(label='Weight Loss')
    reducted_water_consumption = forms.BooleanField(label='Reduced Water Consumption')
    diarrhea = forms.BooleanField(label='Diarrhea')
    less_egg_production = forms.BooleanField(label='Less Egg Production')
    difficulty_breathing = forms.BooleanField(label='Difficulty Breathing')
    pale_comb = forms.BooleanField(label='Pale Comb')
    nasal_discharge = forms.BooleanField(label='Nasal Discharge')
    watery_eyes = forms.BooleanField(label='Watery Eyes')
    paralysis = forms.BooleanField(label='Paralysis')
    watery_feces = forms.BooleanField(label='Watery Feces')

    class Meta:
        model = Predictions
        fields = ['warts', 'loss_of_appetite', 'lesions', 'blister', 'swelling_eyes', 'weight_loss', 'reducted_water_consumption', 'diarrhea', 'less_egg_production', 'difficulty_breathing', 'pale_comb', 'nasal_discharge', 'watery_eyes', 'paralysis', 'watery_feces']
        