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


    def predictInputs(self, inputs):
        try:
            loaded_regressor = joblib.load('random_forest_model.joblib')
            inp = [inputs] #Independent variable
            forecasted_ = loaded_regressor.predict(inp)[0]
            final_val = int(round(float(forecasted_), 3))
            return final_val
        except Exception as e:
            return str(e)
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

                    rs.drop('belongs_to', axis=1, inplace=True)
                    rs.drop('forecasted_disease_id', axis=1, inplace=True)
                    rs.drop('is_correct', axis=1, inplace=True)

                    X = rs.drop(["disease_id"], axis=1).values
                   
                    new_x = np.array(X)

                    X = pd.DataFrame(new_x, columns = ['warts','loss_of_appetite','lesions','blister','swelling_eyes','weight_loss','reduced_water_consumption', 'diarrhea', 'less_egg_production', 'difficulty_breathing', 'pale_comb', 'nasal_discharge', 'watery_eyes', 'paralysis', 'watery_feces'])
                    print("\n\nConverting into pandas dataframe.")
                    y = rs_2.disease_id
                    new_series = pd.Series(y)
                    y = new_series   
                    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=2)
                    tree_model = RandomForestRegressor(n_estimators=3)
                    print("Fitting into Random Forest Tree")
                    tree_model.fit(X_train, y_train)
                    joblib.dump(tree_model, 'random_forest_model.joblib')
                    print("Saving the model.")
                    print("\n\n")
                    for each_rows in X.columns:
                        print(each_rows)
                        time.sleep(0.5)

                    print("Is the dependent variables.")
                    print("Creating a Validation Set from 10% of the Trained Data")
                    self.measureValidation()

                    time.sleep(5)


                    print("Training of machine done.")

        else:
            print("Insufficient Dataset")


    def measureValidation(self):
        Predictor = DatasetGen()

        #GET VALIDATION SET

        query = "SELECT * from app_symptom where belongs_to = 'Training Set' LIMIT (SELECT CAST(ROUND(COUNT(*) * 0.10) AS INTEGER) from app_symptom where belongs_to = 'Training Set');"
        iteration = 0
        count_true = 0
        try:
            result = Symptom.objects.raw(query)
            if len(result) > 0:
                for e in result:


                    inputs = [
                        e.warts, e.loss_of_appetite,e.lesions,
                              e.blister, e.swelling_eyes, e.weight_loss,
                              e.reduced_water_consumption, e.diarrhea, e.less_egg_production,
                              e.difficulty_breathing, e.pale_comb, e.nasal_discharge,
                             e.watery_eyes, e.paralysis, e.watery_feces
                        ]

                    predicted_value = Predictor.predictInputs(inputs)
                    remarks = None

                    if int(predicted_value) == int(e.disease_id):
                        remarks = True
                        count_true = count_true + 1
                    else:
                        remarks = False


                    Symptom.objects.filter(id = int(e.id)).update(belongs_to = 'Validation Set', forecasted_disease = int(predicted_value), is_correct = remarks)
                    iteration = iteration + 1

                #GET TESTING SET
                iteration_testing = 0
                count_testing = 0
                for e in Symptom.objects.raw("SELECT * from app_symptom where belongs_to = 'Testing Set'"):


                    inputs = [
                        e.warts, e.loss_of_appetite,e.lesions,
                              e.blister, e.swelling_eyes, e.weight_loss,
                              e.reduced_water_consumption, e.diarrhea, e.less_egg_production,
                              e.difficulty_breathing, e.pale_comb, e.nasal_discharge,
                             e.watery_eyes, e.paralysis, e.watery_feces
                        ]

                    predicted_value = Predictor.predictInputs(inputs)
                    remarks = None

                    if int(predicted_value) == int(e.disease_id):
                        remarks = True
                        count_testing = count_testing + 1
                    else:
                        remarks = False


                    Symptom.objects.filter(id = int(e.id)).update(belongs_to = 'Testing Set', forecasted_disease = int(predicted_value), is_correct = remarks)
                    iteration_testing = iteration_testing + 1



                from .models import Analysis
                if len(Analysis.objects.all()) < 1:
                    Analysis.objects.create(total_dataset = int(len(Symptom.objects.all())),
                                            validation_set = int(len(Symptom.objects.all()) * 0.8) * 0.10,
                                            training_dataset = int(len(Symptom.objects.all()) * 0.8),
                                            testing_dataset =  int(len(Symptom.objects.all()) * 0.2),
                                            validation_acc = (count_true / iteration) * 100,
                                            testing_acc = (count_testing / iteration_testing) * 100
                                            )
                    print("DONE CREATING ANALYSIS REPORT")
                else:
                    print("DONE UPDATING ANALYSIS REPORT")
                    Analysis.objects.all().update(total_dataset = int(len(Symptom.objects.all())),
                                            validation_set = int(len(Symptom.objects.all()) * 0.8) * 0.10,
                                            training_dataset = int(len(Symptom.objects.all()) * 0.8),
                                            testing_dataset =  int(len(Symptom.objects.all()) * 0.2),
                                            validation_acc = (count_true / iteration) * 100,
                                            testing_acc = (count_testing / iteration_testing) * 100
                                            )


                print("Validation Accuracy: ", (count_true / iteration) * 100, "Testing Accuracy: ", (count_testing / iteration_testing) * 100)


        except Exception as e:
            print(e)


    def measureTesting(self):
        pass


    #MODIFIED 70% 20% 10%
    def getDataSet(self):

        excluded_set = []

        eighty_query = "SELECT * FROM app_symptom LIMIT (SELECT CAST(ROUND(COUNT(*) * 0.8) AS INTEGER) FROM app_symptom);"
        twenty_query = "SELECT * from app_symptom WHERE id not in (SELECT ID FROM app_symptom LIMIT (SELECT CAST(ROUND(COUNT(*) * 0.8) AS INTEGER) FROM app_symptom))"
        

        try:
            if len(ChickenHistory.objects.raw(eighty_query)) > 1:


                for each_rows in ChickenHistory.objects.raw(eighty_query):
                    Symptom.objects.filter(id = int(each_rows.id)).update(belongs_to = 'Training Set')
                    excluded_set.append(int(each_rows.id))

                for each_rows in ChickenHistory.objects.raw(twenty_query):
                    Symptom.objects.filter(id = int(each_rows.id)).update(belongs_to = 'Testing Set')
                    excluded_set.append(int(each_rows.id))


                rs = pd.read_sql(eighty_query, connection)
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
            break
            #self.randomGen()
Scripts()


class TestingSetListCreate(generics.ListCreateAPIView):
    from .models import Symptom
    from .serializers import SymptomsSerializer
    queryset = Symptom.objects.raw('SELECT "app_symptom"."id", "app_symptom"."disease_id", "app_symptom"."warts", "app_symptom"."loss_of_appetite", "app_symptom"."lesions", "app_symptom"."blister", "app_symptom"."swelling_eyes", "app_symptom"."weight_loss", "app_symptom"."reduced_water_consumption", "app_symptom"."diarrhea", "app_symptom"."less_egg_production", "app_symptom"."difficulty_breathing", "app_symptom"."pale_comb", "app_symptom"."nasal_discharge", "app_symptom"."watery_eyes", "app_symptom"."paralysis", "app_symptom"."watery_feces", "app_symptom"."belongs_to", (SELECT name from app_disease where app_disease.id = forecasted_disease_id) as forecasted_disease_id, "app_symptom"."is_correct", "app_disease"."id", "app_disease"."name", "app_disease"."description", "app_disease"."treatment" FROM "app_symptom" LEFT OUTER JOIN "app_disease" ON ("app_symptom"."forecasted_disease_id" = "app_disease"."id") where belongs_to = "Testing Set"')
    serializer_class = SymptomsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']

    def list(self, request, *args, **kwargs):
        from rest_framework.response import Response
        serializer = SymptomsSerializer(self.queryset, many=True)
        return Response(serializer.data)



class ValidationSetListCreate(generics.ListCreateAPIView):
    from .models import Symptom
    from .serializers import SymptomsSerializer
    queryset = Symptom.objects.raw('SELECT "app_symptom"."id", "app_symptom"."disease_id", "app_symptom"."warts", "app_symptom"."loss_of_appetite", "app_symptom"."lesions", "app_symptom"."blister", "app_symptom"."swelling_eyes", "app_symptom"."weight_loss", "app_symptom"."reduced_water_consumption", "app_symptom"."diarrhea", "app_symptom"."less_egg_production", "app_symptom"."difficulty_breathing", "app_symptom"."pale_comb", "app_symptom"."nasal_discharge", "app_symptom"."watery_eyes", "app_symptom"."paralysis", "app_symptom"."watery_feces", "app_symptom"."belongs_to", (SELECT name from app_disease where app_disease.id = forecasted_disease_id) as forecasted_disease_id, "app_symptom"."is_correct", "app_disease"."id", "app_disease"."name", "app_disease"."description", "app_disease"."treatment" FROM "app_symptom" LEFT OUTER JOIN "app_disease" ON ("app_symptom"."forecasted_disease_id" = "app_disease"."id") where belongs_to = "Validation Set"')
    serializer_class = SymptomsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']

    def list(self, request, *args, **kwargs):
        from rest_framework.response import Response
        serializer = SymptomsSerializer(self.queryset, many=True)
        return Response(serializer.data)


class AnalaysisListCreate(generics.ListCreateAPIView):
    from .models import Analysis
    from .serializers import AnalysisSerializer
    queryset = Analysis.objects.all()
    serializer_class = AnalysisSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']


class SymptomsListCreateRandom(generics.ListCreateAPIView):
    from .models import Symptom
    from .serializers import SymptomsSerializer
    queryset = Symptom.objects.all()
    print(queryset.query)

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
        try:

            #VALIDATE THE COUNT
            if len(ChickenHistory.objects.raw(query)) > 0:
                rs = pd.read_sql(query, connection)
                rs = rs.drop(["id"], axis=1)
                print(rs, "HAHA", type(rs))
                return rs
        except Exception as e:
            print(e)
            return None


def getPrediction(request):
    postedValues = []
    

    from django.http import JsonResponse
    def getValue(val):
        if val.lower() == "true":
            return True
        elif val.lower() == "false":
            return False






    def getPredictedDisease(id):
        from .models import Disease

        try:
            for each in Disease.objects.filter(id = int(str(id))):
                print(each)
                return str(each.name)
        except Exception as e:
            return str(e)


    def predictValues(inputs):
        voted_predictions = ""

        try:

            loaded_regressor = joblib.load('random_forest_model.joblib')
            inp = [inputs] #Independent variable
            forecasted_ = loaded_regressor.predict(inp)[0]
            final_val = int(round(float(forecasted_), 6))
            fval = getPredictedDisease(final_val)

            for tree in loaded_regressor.estimators_:
                prediction = tree.predict(inp)[0]
                predictions.append(getPredictedDisease(int(round(float(prediction), 6))))

            for each_rows in predictions:
                voted_predictions = voted_predictions  + str(each_rows) + "<br>"

            #return "Votes from 3 Trees:" + "<br><br>" +  str(voted_predictions)[0:len(voted_predictions)] + "Final Verdict: <br>" + str(fval)
            return "Final Verdict: <br>" + str(fval)
        except Exception as e:
            return str(e)


    if request.method == 'POST':
        predictions = []
        try:
                
                for each_rows in request.POST:
                    print(request.POST.get(str(each_rows)))
                    postedValues.append(getValue(request.POST.get(str(each_rows))))

                message = predictValues(postedValues)

                response_data = {'message': message}
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
