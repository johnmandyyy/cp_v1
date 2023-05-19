"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse

from .forms import *


from rest_framework import generics
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from django.db import connection

from threading import Thread
import pandas
import time

#IMPORT DEEP LEARNING NEEDS
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import joblib


class Scripts(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start() 




    def startAlgorithm(self):
        if self.getDataSet() != None:
            vaccine, morning_bath, afternoon_bath, va, vd, ve, vk, b1, infected = self.getDataSet()


            #ADD ENCODER TO MAKE SURE TREE WOULD WORK EVEN IF IT IS A STRING
            encoder = LabelEncoder()

            #FIT TO THE ENCODER
            vaccine_encoded = encoder.fit_transform(vaccine)
            morning_bath_encoded = encoder.fit_transform(morning_bath)
            afternoon_bath_encoded = encoder.fit_transform(afternoon_bath)
            va_encoded = encoder.fit_transform(va)
            vd_encoded = encoder.fit_transform(vd)
            ve_encoded = encoder.fit_transform(ve)
            vk_encoded = encoder.fit_transform(vk)
            vb1_encoded = encoder.fit_transform(b1)
            infected_encoded = encoder.fit_transform(infected)

            print("DONE ENCODING")

            # CREATE PANDAS DATAFRAME
            data = pd.DataFrame({
                'vaccine': vaccine_encoded,
                'morning_bath': morning_bath_encoded,
                'afternoon_bath': afternoon_bath_encoded,
                'va': va_encoded,
                'vd': vd_encoded,
                've': ve_encoded,
                'vk': vk_encoded,
                'b1': vb1_encoded,
                'infected': infected_encoded
            })

            print(data)


            # Create the random forest regressor
            regressor = RandomForestRegressor(n_estimators=3)  # Set the number of trees to 3

            # Split the data into independent and dependent variables
            X = data[['vaccine', 'morning_bath', 'afternoon_bath', 'va', 'vd', 've', 'vk', 'b1']]
            y = data['infected']

            # Fit the regressor to the data
            regressor.fit(X, y)

            #SAVE MODEL
            joblib.dump(regressor, 'random_forest_model.joblib')
            print("Model was saved.")


    def getDataSet(self):

        #DEFINE INDEPDENT VARIABLES WHICH ARE THE ROUTINES
        vaccine = []
        morning_bath = []
        afternoon_bath = []
        va = []
        vd = []
        ve = []
        vk = []
        b1 = []
        #DEFINE THE DEPENDENT VARIABLE WHICH IS THE PREDICTING OUTPUT
        infected = []

        #GET THE DATASET
        query = 'SELECT "app_chickenhistory"."id", "app_chickenhistory"."chicken_id", "app_chickenhistory"."is_morning_bath", "app_chickenhistory"."is_afternoon_bath", "app_chickenhistory"."is_vitamin_a", "app_chickenhistory"."is_vitamin_d", "app_chickenhistory"."is_vitamin_e", "app_chickenhistory"."is_vitamin_k", "app_chickenhistory"."is_vitamin_b1", "app_chickenhistory"."date", "app_chickens"."id", "app_chickens"."tag_number", "app_chickens"."fowl_pox_vaccine", "app_chickens"."birthdate", "app_chickens"."is_infected", "app_chickens"."picture", "app_chickens"."verdict" FROM "app_chickenhistory" INNER JOIN "app_chickens" ON ("app_chickenhistory"."chicken_id" = "app_chickens"."id")'
        try:

            #VALIDATE THE COUNT
            if len(ChickenHistory.objects.raw(query)) > 0:

                #IF THERE IS A DATASET ADD THE DATA 
                for each_rows in ChickenHistory.objects.raw(query):

                    #ADDING EACH DATA TO THE LIST PER ROW
                    vaccine.append(str(each_rows.fowl_pox_vaccine))
                    morning_bath.append(str(each_rows.is_morning_bath))
                    afternoon_bath.append(str(each_rows.is_afternoon_bath))
                    va.append(str(each_rows.is_vitamin_a))
                    vd.append(str(each_rows.is_vitamin_d))
                    ve.append(str(each_rows.is_vitamin_e))
                    vk.append(str(each_rows.is_vitamin_k))
                    b1.append(str(each_rows.is_vitamin_b1))
                    infected.append(str(each_rows.is_infected))

                return vaccine, morning_bath, afternoon_bath, va, vd, ve, vk, b1, infected
            else:
                return None
        except Exception as e:
            return None
            print(e)



    def run(self):

        while True:
            print("Haha")
            time.sleep(1)
            self.startAlgorithm()

Scripts()



class ChickensListCreateView(generics.ListCreateAPIView):
    queryset = Chickens.objects.all()
    serializer_class = ChickensSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_infected']

class ChickensRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chickens.objects.all()
    serializer_class = ChickensSerializer
    lookup_field = 'id'  # Set the lookup_field to 'id'


class ChickenHistoryListCreateView(generics.ListCreateAPIView):
    serializer_class = ChickenHistorySerializerJoined
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']

    def get_queryset(self):
        return ChickenHistory.objects.all().select_related('chicken')

class ChickenHistoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChickenHistory.objects.all()
    serializer_class = ChickenHistorySerializer
    lookup_field = 'id'




def setCurrentValues(id):

        #DEFINE INDEPDENT VARIABLES WHICH ARE THE ROUTINES
        vaccine = []
        morning_bath = []
        afternoon_bath = []
        va = []
        vd = []
        ve = []
        vk = []
        b1 = []
        #DEFINE THE DEPENDENT VARIABLE WHICH IS THE PREDICTING OUTPUT
        infected = []

        #GET THE DATASET
        query = 'SELECT "app_chickenhistory"."id", "app_chickenhistory"."chicken_id", "app_chickenhistory"."is_morning_bath", "app_chickenhistory"."is_afternoon_bath", "app_chickenhistory"."is_vitamin_a", "app_chickenhistory"."is_vitamin_d", "app_chickenhistory"."is_vitamin_e", "app_chickenhistory"."is_vitamin_k", "app_chickenhistory"."is_vitamin_b1", "app_chickenhistory"."date", "app_chickens"."id", "app_chickens"."tag_number", "app_chickens"."fowl_pox_vaccine", "app_chickens"."birthdate", "app_chickens"."is_infected", "app_chickens"."picture", "app_chickens"."verdict" FROM "app_chickenhistory" INNER JOIN "app_chickens" ON ("app_chickenhistory"."chicken_id" = "app_chickens"."id") WHERE app_chickenhistory.id = ' + "'" + str(id) + "'"  
        print(query)
        try:

            #VALIDATE THE COUNT
            if len(ChickenHistory.objects.raw(query)) > 0:

                #IF THERE IS A DATASET ADD THE DATA 
                for each_rows in ChickenHistory.objects.raw(query):

                    #ADDING EACH DATA TO THE LIST PER ROW
                    vaccine.append(str(each_rows.fowl_pox_vaccine))
                    morning_bath.append(str(each_rows.is_morning_bath))
                    afternoon_bath.append(str(each_rows.is_afternoon_bath))
                    va.append(str(each_rows.is_vitamin_a))
                    vd.append(str(each_rows.is_vitamin_d))
                    ve.append(str(each_rows.is_vitamin_e))
                    vk.append(str(each_rows.is_vitamin_k))
                    b1.append(str(each_rows.is_vitamin_b1))
                    infected.append(str(each_rows.is_infected))

                return vaccine, morning_bath, afternoon_bath, va, vd, ve, vk, b1, infected
            else:
                return None
        except Exception as e:
            return None
            print(e)


def getPrediction(request):

    from django.http import JsonResponse
    def getValue(val):
        if val.lower() == "true":
            return True
        elif val.lower() == "false":
            return False

    if request.method == 'POST':
        
        lst = None
        try:

            from django.utils import timezone
            if len(ChickenHistory.objects.filter(chicken = int(request.POST.get('chicken')), date = timezone.now())) > 0:
                response_data = {'message': 'Chicken has an existing routine for today.'}
                return JsonResponse(response_data)

            new_history = ChickenHistory.objects.create(chicken = Chickens.objects.get(id=request.POST.get('chicken')),
                                         is_morning_bath = getValue(str(request.POST.get('is_morning_bath').title())),
                                         is_afternoon_bath = getValue(str(request.POST.get('is_afternoon_bath').title())),
                                         is_vitamin_a = getValue(str(request.POST.get('is_vitamin_a').title())),
                                         is_vitamin_d = getValue(str(request.POST.get('is_vitamin_d').title())),
                                         is_vitamin_e = getValue(str(request.POST.get('is_vitamin_e').title())),
                                         is_vitamin_k = getValue(str(request.POST.get('is_vitamin_k').title())),
                                         is_vitamin_b1 = getValue(str(request.POST.get('is_vitamin_b1').title())),
                                         date=timezone.now()
                                          )
            
            new_history_id = new_history.id
            print(new_history_id)
            if setCurrentValues(new_history_id) != None:
                
                vaccine, morning_bath, afternoon_bath, va, vd, ve, vk, b1, infected = setCurrentValues(new_history_id)
   
                #ADD ENCODER TO MAKE SURE TREE WOULD WORK EVEN IF IT IS A STRING
                encoder = LabelEncoder()

                #FIT TO THE ENCODER
                vaccine_encoded = encoder.fit_transform(vaccine)
                morning_bath_encoded = encoder.fit_transform(morning_bath)
                afternoon_bath_encoded = encoder.fit_transform(afternoon_bath)
                va_encoded = encoder.fit_transform(va)
                vd_encoded = encoder.fit_transform(vd)
                ve_encoded = encoder.fit_transform(ve)
                vk_encoded = encoder.fit_transform(vk)
                vb1_encoded = encoder.fit_transform(b1)


                data = pd.DataFrame({
                    'vaccine': vaccine_encoded,
                    'morning_bath': morning_bath_encoded,
                    'afternoon_bath': afternoon_bath_encoded,
                    'va': va_encoded,
                    'vd': vd_encoded,
                    've': ve_encoded,
                    'vk': vk_encoded,
                    'b1': vb1_encoded
                })

                loaded_regressor = joblib.load('random_forest_model.joblib')
                # Use the loaded model for prediction
                loaded_prediction = loaded_regressor.predict(data)
                loaded_prediction_label = encoder.inverse_transform([int(loaded_prediction)])[0]

                # Make a prediction using the loaded regressor for each tree in the forest
                loaded_predictions = []
                for tree in loaded_regressor.estimators_:
                    loaded_prediction = tree.predict(data)
                    loaded_predictions.append(loaded_prediction)

                # Voting
                loaded_votes = [encoder.inverse_transform([int(p)])[0] for p in loaded_predictions]
                loaded_casted_votes = ", ".join(loaded_votes)
                loaded_final_vote = max(set(loaded_votes), key=loaded_votes.count)

                print("Predictions from each tree (loaded model):")
                print(loaded_casted_votes)
                print("Final Vote (loaded model):")
                print(type(loaded_final_vote))


                if str(loaded_final_vote).lower() == "false":
                    loaded_final_vote = "Chicken is not sick no isolation needed."
                elif str(loaded_final_vote).lower() == "true":
                    loaded_final_vote = "Chicken is sick isolation is needed from other chickens."

                if getValue(str(loaded_final_vote)) == True:
                    Chickens.objects.filter(id = int(request.POST.get('chicken'))).update(verdict = "Possibly Sick")
                elif getValue(str(loaded_final_vote)) == False:
                    Chickens.objects.filter(id = int(request.POST.get('chicken'))).update(verdict = "Not Sick")    
                    
                response_data = {'message':  "Votes from 3 trees: "+ str(loaded_casted_votes) + "<br>Final Vote:" + str(loaded_final_vote)}
                return JsonResponse(response_data)
    
        except Exception as e:
            print(e)


    else:
        response_data = {'message': 'Not a POST'}
        return JsonResponse(response_data)
    
    
 




def home(request):
    """Renders the home page."""


    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
            'add_chicken': ChickensForm(),
            'add_history': ChickenHistoryForm(),
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
