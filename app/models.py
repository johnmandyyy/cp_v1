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
    picture = models.ImageField(upload_to='media/chicken_pictures', null=True)
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

