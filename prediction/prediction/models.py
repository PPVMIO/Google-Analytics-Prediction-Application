from django.db import models
from jsonfield import JSONField
from sklearn.ensemble import RandomForestClassifier

class Model_RF(models.Model):
    output_data_json = JSONField()
    time_stamp = models.DateTimeField('date published')
    def __str__(self):
        return str(self.time_stamp)
    
class Dog(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name