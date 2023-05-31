"""
Definition of models.
"""

from django.db import models

# Create your models here.


from django.db import models

class Chickens(models.Model):
    tag_number = models.PositiveIntegerField(unique=True)
    fowl_pox_vaccine = models.BooleanField(default=False)
    birthdate = models.DateField(default=models.DateField(auto_now_add=True))
    is_infected = models.BooleanField(default=False)
    picture = models.ImageField(upload_to='chicken_pictures', null=True)
    verdict = models.CharField(max_length=255, default='No Verdict', null = False)

    def __str__(self):
        return "Tag Number: " + str(self.tag_number)

class ChickenHistory(models.Model):
    chicken = models.ForeignKey(Chickens, on_delete=models.CASCADE)
    is_morning_bath = models.BooleanField(default=False)
    is_afternoon_bath = models.BooleanField(default=False)
    is_vitamin_a = models.BooleanField(default=False)
    is_vitamin_d = models.BooleanField(default=False)
    is_vitamin_e = models.BooleanField(default=False)
    is_vitamin_k = models.BooleanField(default=False)
    is_vitamin_b1 = models.BooleanField(default=False)
    date = models.DateField(default=models.DateField(auto_now=True), null = True)


    def __str__(self):
        return self.chicken.__str__()


class Disease(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null = True, default = None)
    treatment = models.TextField(null = True, default = None)
    def __str__(self):
        return self.name

class Symptom(models.Model):

    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    warts = models.BooleanField(default=False)
    loss_of_appetite = models.BooleanField(default=False)
    lesions = models.BooleanField(default=False)
    blister = models.BooleanField(default=False)
    swelling_eyes = models.BooleanField(default=False)
    weight_loss = models.BooleanField(default=False)
    reduced_water_consumption = models.BooleanField(default=False)
    diarrhea = models.BooleanField(default=False)
    less_egg_production = models.BooleanField(default=False)
    difficulty_breathing = models.BooleanField(default=False)
    pale_comb = models.BooleanField(default=False)
    nasal_discharge = models.BooleanField(default=False)
    watery_eyes = models.BooleanField(default=False)
    paralysis = models.BooleanField(default=False)
    watery_feces = models.BooleanField(default=False)

    belongs_to = models.CharField(max_length = 100, default = 'No Category')
    forecasted_disease = models.ForeignKey(Disease, on_delete=models.CASCADE, null = True, related_name = 'forecasted_disease')
    is_correct = models.BooleanField(null = True)

    def __str__(self):
        return f"Symptoms of {self.disease.name}"


class Predictions(models.Model):

    warts = models.BooleanField(default=False)
    loss_of_appetite = models.BooleanField(default=False)
    lesions = models.BooleanField(default=False)
    blister = models.BooleanField(default=False)
    swelling_eyes = models.BooleanField(default=False)
    weight_loss = models.BooleanField(default=False)
    reduced_water_consumption = models.BooleanField(default=False)
    diarrhea = models.BooleanField(default=False)
    less_egg_production = models.BooleanField(default=False)
    difficulty_breathing = models.BooleanField(default=False)
    pale_comb = models.BooleanField(default=False)
    nasal_discharge = models.BooleanField(default=False)
    watery_eyes = models.BooleanField(default=False)
    paralysis = models.BooleanField(default=False)
    watery_feces = models.BooleanField(default=False)
    verdict = models.ForeignKey(Disease, on_delete=models.CASCADE, null = True)

    def __str__(self):
        return f"Symptoms of {self.disease.name}"


class Analysis(models.Model):

    total_dataset = models.IntegerField(default = 0, null = False)
    validation_set = models.IntegerField(default = 0, null = False)
    training_dataset = models.IntegerField(default = 0, null = False)
    testing_dataset = models.IntegerField(default = 0, null = False)

    validation_acc = models.FloatField(default = 0, null = False)
    testing_acc = models.FloatField(default = 0, null = False)