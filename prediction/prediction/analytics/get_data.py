"""Hello Analytics Reporting API V4."""

import argparse
import json
import pprint
import csv

import os
cwd = os.getcwd()
print(cwd)

from apiclient.discovery import build
import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools

from datetime import datetime, timedelta

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/$discovery/rest')
CLIENT_SECRETS_PATH = 'ga_input/client_secrets.json' # Path to client_secrets.json file.
VIEW_ID = ''




def initialize_analyticsreporting():
    """Initializes the analyticsreporting service object.
    Returns: analytics an authorized analyticsreporting service object.
    """
    # Parse command-line arguments.
    parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      parents=[tools.argparser])
    flags = parser.parse_args([])

    # Set up a Flow object to be used if we need to authenticate.
    flow = client.flow_from_clientsecrets(
      CLIENT_SECRETS_PATH, scope=SCOPES,
      message=tools.message_if_missing(CLIENT_SECRETS_PATH))

    # Prepare credentials, and authorize HTTP object with them.
    # If the credentials don't exist or are invalid run through the native client
    # flow. The Storage object will ensure that if successful the good
    # credentials will get written back to a file.
    storage = file.Storage('analyticsreporting.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, flags)
    http = credentials.authorize(http=httplib2.Http())

    # Build the service object.
    analytics = build('analytics', 'v4', http=http, discoveryServiceUrl=DISCOVERY_URI)

    return analytics


def get_report(analytics, viewID, dims, metrs, date_range):
    # Use the Analytics Service Object to query the Analytics Reporting API V4.

    # Use default date range unless otherwise specified
    startDate = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
    endDate = datetime.now().strftime("%Y-%m-%d")
    if len(date_range) == 2:
        startDate = date_range[0]
        endDate = date_range[1]
        
    dimensions = []
    for d in dims:
        dimensions.append({"name": str(d), "histogramBuckets":[]})
    metrics = []
    for m in metrs:
        metrics.append({"expression": str(m)})    
    return analytics.reports().batchGet(
      body={
        "reportRequests":[
        {
            "viewId": viewID,
            "dateRanges": [{"startDate": startDate, "endDate": endDate}],
            "dimensions": dimensions,
            "metrics": metrics,
            "pageSize": "10000"
        }
      ]
    }
  ).execute()
  

def export_data(response):
    output_str = ''
    
    reports = response['reports']
    
    column_header = reports[0]['columnHeader']
    dim_names = column_header['dimensions']
    metric_header = column_header['metricHeader']
    metric_header_entries = metric_header['metricHeaderEntries']
    metric_names = []
    for entry in metric_header_entries:
        metric_names.append(entry['name'])
        
    data = reports[0]['data']
    rows = data['rows']
    
    metric_values = []
    dim_values = []
    for r in rows:
        metric_values.append(r['metrics'][0]['values'])
        dim_values.append(r['dimensions'])
        
    print(metric_values[6241])
    print(dim_values[6241])

    
    col_str = ''
    for mn in metric_names:
        col_str = col_str + mn + '|'
    for dn in dim_names:
        col_str = col_str + dn + '|'
    col_str = col_str.rstrip('|')
    col_str = col_str + '\n'
    
    value_str = ''
    for m_row, d_row in zip(metric_values, dim_values):
        for mv in m_row:
            value_str = value_str + mv + '|'
        for dv in d_row:
            value_str = value_str + dv + '|'
        value_str = value_str.rstrip('|')
        value_str = value_str + '\n'
    value_str = value_str.rstrip('\n')
    
    

    output_str = col_str + value_str
    output_file_name = 'analytics_data/exported_data.csv'
    text_file = open(output_file_name, 'w')
    text_file.write(output_str)
    text_file.close() 

    
def pull_data(viewID, cat_dimensions, dimensions, metrics, date_range):
    print('\n***PULL DATA***\n')
    
    print('GET_DATA viewID', viewID)
    print('GET_DATA cat_dimensions', cat_dimensions)
    print('GET_DATA dimensions', dimensions)
    print('GET_DATA metrics', metrics)
    print('GET_DATA dateRange', date_range)
    all_dimensions = cat_dimensions + dimensions

    analytics = initialize_analyticsreporting()
    response = get_report(analytics, viewID, all_dimensions, metrics, date_range)
    export_data(response)
    print('EXPORT SUCCESSFUL')
    


    


