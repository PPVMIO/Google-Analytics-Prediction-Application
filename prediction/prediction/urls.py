from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'classification', views.classification, name='classification'),
    url(r'results', views.results, name='results'),
    url(r'models/random-forest/', views.model_rf, name='model_rf')

]


"""
urlpatterns = [
    # ex: /polls/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /polls/5/
    url(r'classification', views.ClassificationView.as_view(), name='classification'),
    # ex: /polls/5/results/
    url(r'results', views.ResultsView.as_view(), name='results'),
    # ex: /polls/5/vote/
    #url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
"""



