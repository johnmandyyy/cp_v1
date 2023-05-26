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




class DatasetGen:

    def __init__(self):
        pass


    def randomGen(self):
        from .models import Disease, Symptom
        list_of_ids = []
        for each_rows in Disease.objects.all():
            list_of_ids.append(int(str(each_rows.id)))

        list_of_ids.sort()

        import random
        disease = []

        def random_bool():
            return random.choice([True, False])

        Symptom.objects.all().delete()
   
        i = 0
        while i < 1095:

            Symptom.objects.create(disease = Disease.objects.get(id = random.choice(list_of_ids)),
                                   warts = random_bool(),
                                   loss_of_appetite = random_bool(),
                                   lesions = random_bool(),
                                   blister = random_bool(),
                                   swelling_eyes = random_bool(),
                                   weight_loss = random_bool(),
                                   reduced_water_consumption = random_bool(),
                                   diarrhea = random_bool(),
                                   less_egg_production = random_bool(),
                                   difficulty_breathing = random_bool(),
                                   pale_comb = random_bool(),
                                   nasal_discharge = random_bool(),
                                   watery_eyes = random_bool(),
                                   paralysis = random_bool(),
                                   watery_feces = random_bool(),
                                   )

            i = i + 1


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
                    X = rs.drop(["disease_id"], axis=1).values
                    new_x = np.array(X)

                    X = pd.DataFrame(new_x, columns = ['warts','loss_of_appetite','lesions','blister','swelling_eyes','weight_loss','reduced_water_consumption', 'diarrhea', 'less_egg_production', 'difficulty_breathing', 'pale_comb', 'nasal_discharge', 'watery_eyes', 'paralysis', 'watery_feces'])
                    y = rs_2.disease_id
                    new_series = pd.Series(y)
                    y = new_series   
                    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=2)
                    tree_model = RandomForestRegressor(n_estimators=3)
                    tree_model.fit(X_train, y_train)
                    joblib.dump(tree_model, 'random_forest_model.joblib')

                    print(X.columns, X.dtypes)
                    print("Training of machine done.")

        else:
            print("Insufficient Dataset")


    def getDataSet(self):
        query = 'SELECT * from app_symptom'
        try:
            if len(ChickenHistory.objects.raw(query)) > 1:
                rs = pd.read_sql(query, connection)
                return rs
            else:
                return None
        except Exception as e:
            print(e)
            return None
            



    def run(self):

        while True:
            time.sleep(1)
            self.startAlgorithm()
            #self.randomGen()
Scripts()


class SymptomsListCreateRandom(generics.ListCreateAPIView):
    from .models import Symptom
    from .serializers import SymptomsSerializer
    queryset = Symptom.objects.all()
    serializer_class = SymptomsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']

    def list(self, request, *args, **kwargs):
        from rest_framework.response import Response
        Symptom.objects.all().delete()
        RandomData = DatasetGen()
        RandomData.randomGen()
        serializer = SymptomsSerializer(Symptom.objects.all(), many=True)
        return Response(serializer.data)

class SymptomsListCreateView(generics.ListCreateAPIView):
    from .models import Symptom
    from .serializers import SymptomsSerializer
    queryset = Symptom.objects.all()
    serializer_class = SymptomsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']


class SymptomsDestroyAll(generics.ListCreateAPIView):
    from .models import Symptom
    from .serializers import SymptomsSerializer
    queryset = Symptom.objects.all()
    serializer_class = SymptomsSerializer


    def list(self, request, *args, **kwargs):
        Symptom.objects.all().delete()
        return super().list(request, *args, **kwargs)

class DiseaseListCreateView(generics.ListCreateAPIView):
    from .models import Disease
    from .serializers import DiseaseSerializer
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']

class DiseaseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    from .models import Disease
    from .serializers import DiseaseSerializer
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']


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

        try:
                pass
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
    from .forms import PredictionSymptomsForm

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
            'add_chicken': ChickensForm(),
            'prediction_form' : PredictionSymptomsForm(),
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
    from .forms import DiseasesForm
    from .forms import SymptomsForm

    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'symptoms_form' : SymptomsForm,
            'disease_form': DiseasesForm,
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
