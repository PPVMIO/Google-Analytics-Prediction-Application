from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template import loader

from django.core.management import call_command

from django.urls import reverse
from django.views import generic

from django.utils import timezone
from .models import Dog, Model_RF
import urllib, json
import pandas as pd



def index(request):
    useless_str = 'this is some useless str on the index page'
    template = loader.get_template('prediction/index.html')
    context = {
        'useless_str': useless_str,
    }
    return HttpResponse(template.render(context, request))

def classification(request):
    useless_str = 'this is some useless str on the index page'
    template = loader.get_template('prediction/classification.html')
    context = {
        'useless_str': useless_str,
    }
    return HttpResponse(template.render(context, request))

def results(request):
    
    #uses pickle to save json object for future use
    from six.moves import cPickle
    get_params = {}
    template = loader.get_template('prediction/results.html')
    if request.GET:
        print('using pickle')
        print('get parameters set')
        print(request.GET)
        
        with open('analytics_data/opt.clf', 'rb') as f:
            clf = cPickle.load(f)
            
        
        url = 'http://localhost:8000/prediction/models/random-forest/'
        json_data = ''
        with urllib.request.urlopen(url) as u:
            json_data = json.loads(u.read().decode())
        
        dummy_dimensions = json_data['originalData']['dimensionData']['dummyDimensions']
        prediction_dict = {}
        print('len of dummy dims', len(dummy_dimensions))
        #print('dummy dim len before first loop', len(dummy_dimensions))
        for k, v in get_params.items():
            search_dimension = str(k + '_' + v[0])
            #print(search_dimension)
            if search_dimension in dummy_dimensions:
                #print('***MATCH***')
                prediction_dict[search_dimension] = 1
                dummy_dimensions.remove(search_dimension)
                
        print('dummy dim len after first loop', len(dummy_dimensions))
        #print('pred_dict before second loop', prediction_dict)
        sum = 0
        for d in dummy_dimensions:
            prediction_dict[d] = 0
            #dummy_dimensions = dummy_dimensions.remove(d)
            sum += 1
        print('sum is', sum)
        print('dummy dim size at end:', len(dummy_dimensions))
        #print(dict(list(prediction_dict.items())[0:2]))
        #print('pred_dict after second loop', prediction_dict)
        print(len(prediction_dict))
        #predict_df = pd.DataFrame.from_dict(prediction_dict)
        predict_df = pd.DataFrame(prediction_dict, index=[0])
        #print(predict_df.head())
        predict_val = clf.predict(predict_df)
        print(clf.predict(predict_df))
        
        params = {
            'dimensions': dict(request.GET),
            'predict_val': predict_val
        }

            
        
        print('get params', params)
        return HttpResponse(template.render(params, request))
        
    
        
        
    else:
        print('no pickle')
        
        #BEGIN MODEL BUILDING
        print('building model')
        from prediction.analytics import get_data, clf_random_forest
        

        cat_dimensions = request.POST.getlist('dim_cat')
        print('cat dimensions:', cat_dimensions)
        dimensions = request.POST.getlist('dim')
        print('dimensions:', dimensions)
        metrics = request.POST.getlist('metrics')
        print('metrics:', metrics)
        info = request.POST
        start_date = request.POST['startDate']
        end_date = request.POST['endDate']
        viewID = request.POST['viewID']
        date_range = [start_date, end_date]
        print('date range:', date_range)
        get_data.pull_data(viewID, cat_dimensions, dimensions, metrics, [start_date, end_date])
        output_data, opt_clf = clf_random_forest.build_model(dimensions, cat_dimensions, metrics, date_range)
        Model_RF(output_data_json=output_data,  time_stamp=timezone.now()).save()
        with open('analytics_data/opt.clf', 'wb') as f:
            cPickle.dump(opt_clf, f)
        
        
        
        
        #params = {"all_variables": dimensions + cat_dimensions + metrics}
        
        return HttpResponse(template.render(request))
    #END MODEL BUILDING 
    #print(output_data)
        



def model_rf(request):
    return JsonResponse(Model_RF.objects.order_by('-id')[0].output_data_json)
 
    


