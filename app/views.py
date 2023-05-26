"""
Definition of views.
"""
import numpy as np
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse

from .forms import *
from sklearn.model_selection import train_test_split



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
        redo = 0
        if type(self.getDataSet()) != type(None):

                if redo == 1:
                    pass
                else:
                    
                    rs = self.getDataSet()
                   
                    rs_2 = rs
                    rs.drop('id', axis=1, inplace=True)
                    X = rs.drop(["is_infected"], axis=1).values
                    new_x = np.array(X)
                    print(new_x, "IS THE NEW")
                    X = pd.DataFrame(new_x, columns = ['is_morning_bath','is_afternoon_bath','is_vitamin_a','is_vitamin_d','is_vitamin_e','is_vitamin_k','is_vitamin_b1', 'fowl_pax_vaccine'])
                    y = rs_2.is_infected
                    new_series = pd.Series(y)
                    y = new_series   
                    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=2)
                    tree_model = RandomForestRegressor(n_estimators=3)
                    tree_model.fit(X_train, y_train)
                    joblib.dump(tree_model, 'random_forest_model.joblib')
                    print("Training of machine done.")

        else:
            print("Insufficient Dataset")


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
        query = 'SELECT "app_chickenhistory".id, "app_chickenhistory"."is_morning_bath", "app_chickenhistory"."is_afternoon_bath", "app_chickenhistory"."is_vitamin_a", "app_chickenhistory"."is_vitamin_d", "app_chickenhistory"."is_vitamin_e", "app_chickenhistory"."is_vitamin_k", "app_chickenhistory"."is_vitamin_b1", "app_chickens"."fowl_pox_vaccine", "app_chickens"."is_infected" FROM "app_chickenhistory" INNER JOIN "app_chickens" ON ("app_chickenhistory"."chicken_id" = "app_chickens"."id")'
        try:

            #VALIDATE THE COUNT
            if len(ChickenHistory.objects.raw(query)) > 1:
                rs = pd.read_sql(query, connection)
               
                return rs

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
            print(e)
            return None
            



    def run(self):

        while True:
            time.sleep(5)
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
        query = 'SELECT "app_chickenhistory"."id", "app_chickenhistory"."is_morning_bath", "app_chickenhistory"."is_afternoon_bath", "app_chickenhistory"."is_vitamin_a", "app_chickenhistory"."is_vitamin_d", "app_chickenhistory"."is_vitamin_e", "app_chickenhistory"."is_vitamin_k", "app_chickenhistory"."is_vitamin_b1", "app_chickens"."fowl_pox_vaccine" FROM "app_chickenhistory" INNER JOIN "app_chickens" ON ("app_chickenhistory"."chicken_id" = "app_chickens"."id") WHERE app_chickenhistory.id = ' + "'" + str(id) + "'"  
        print(query)
        try:

            #VALIDATE THE COUNT
            if len(ChickenHistory.objects.raw(query)) > 0:
                rs = pd.read_sql(query, connection)
                print(rs.dtypes)
                rs = rs.drop(["id"], axis=1)
                print(rs, "HAHA", type(rs))
                return rs
        except Exception as e:
            print(e)
            return None


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
            if type(setCurrentValues(new_history_id)) != type(None):
 
                data = setCurrentValues(new_history_id).values
                loaded_regressor = joblib.load('random_forest_model.joblib')
                # Use the loaded model for prediction
                predictions_ = []
                vrd = ""
                for idx, tree in enumerate(loaded_regressor.estimators_):
                    print(f"Votes from Tree {idx+1}:")
                    print(tree.predict(data), type(tree.predict(data)), )
                    if int(tree.predict(data)) == 1:
                        vrd = vrd + "Sick" + ","
                    else:
                        vrd = vrd + "Not Sick" + ","
        

                # Print the final vote
                final_vote = loaded_regressor.predict(data)
                print("Final Vote:")
                if final_vote[0] > 0.60:
                    loaded_final_vote = "true"
                else:
                    loaded_final_vote = "false"


                if getValue(str(loaded_final_vote)) == True:
                    Chickens.objects.filter(id = int(request.POST.get('chicken'))).update(verdict = "Possibly Sick")
                elif getValue(str(loaded_final_vote)) == False:
                    Chickens.objects.filter(id = int(request.POST.get('chicken'))).update(verdict = "Not Sick")    

                if str(loaded_final_vote).lower() == "false":
                    loaded_final_vote = "Chicken is not sick no isolation needed."
                elif str(loaded_final_vote).lower() == "true":
                    loaded_final_vote = "Chicken is sick isolation is needed from other chickens."

                    
                response_data = {'message':  "Votes from 3 trees: "+ str(vrd) + "<br>Final Vote:" + str(loaded_final_vote)}
                return JsonResponse(response_data)
    
        except Exception as e:
             response_data = {'message': e}
             return JsonResponse(response_data)
            

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
