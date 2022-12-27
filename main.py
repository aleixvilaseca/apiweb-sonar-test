import requests
import json
import sys
import constants
import openpyxl
import os
import urllib3
import pyslurpers
from sonarqube import SonarQubeClient
from openpyxl.workbook import workbook
from requests.auth import HTTPBasicAuth
from os.path import exists
from django.http import HttpResponse
from tqdm import tqdm as pretty_progress_bar


def get_values(request, key_list, sonar, total, measure, value, ncloc): 
    
    """Get the number of vulnerabilities per project and write them to a file"""
    print('Connection to Sonarqube')
    url = "https://codi.qualitat.solucions.gencat.cat/"
    username = constants.SONAR_USER
    password = constants.SONAR_PASSWORD
    sonar = SonarQubeClient(url, username, password)

    print('Getting all projects')
    sonar = list(sonar.projects.search_projects()) # search all sonarqube projects
        
    key_list = []
    for key in sonar:
        key_list.append(key['key']) # append the project key to a list

    for key in range(len(key_list)):
        (key_list[key]) = ''.join([key for key in key_list if key != [constants.APPLICATIONS_TO_EXCLUDE]]) # fer servir replace
        if key_list[key] == '0192-0206-tributs':
            key_list[key] = key_list[key].replace('0192-', '', 1)
            with open('reports/new_list.txt', 'a') as f:
                f.write(' %s:%s \r      ' %(key, key_list[key]))

    key_list = str(key_list).replace('[', '').replace(']', '').replace("'", "").replace(" ", "").split(',') # remove the brackets from the list (not needed for the API

    print('Getting values for project') 
    
    try:      
        for key in key_list:
            if key is not None:
                
                api_url_sev = requests.get("https://codi.qualitat.solucions.gencat.cat/api/measures/component?component=%s&metricKeys=ncloc&ps=100" %(key), auth=HTTPBasicAuth(username, password))

                if api_url_sev.status_code == 200:
                    data = api_url_sev.json()
                    ncloc = data["component"]["measures"][0]["value"]
                    #ncloc = int(data["component"]["measures"][0]["value"])
                    with open('reports/ncloc.txt', 'a') as f:
                        f.write(' %s: %s \r      ' %(key, ncloc))

                else:
                    print('Error: %s:%s' %(key, api_url_sev.status_code))

        for key in key_list:
            if key is not None:
                
                api_url_sev = requests.get("https://codi.qualitat.solucions.gencat.cat/api/measures/component?component=%s&metricKeys=sqale_debt_ratio&ps=100" %(key), auth=HTTPBasicAuth(username, password))

                if api_url_sev.status_code == 200:
                    data = api_url_sev.json()
                    
                    value = data["component"]["measures"][0]["value"]
                    value = float(data["component"]["measures"][0]["value"])
                    value = value / 60
                    value = value / 8
                    value = (value / (ncloc * 0.06)) * 100
                    with open('reports/technical_debt.txt', 'a') as f:
                        f.write(' %s: %s \r      ' %(key, value))    
                else:
                    print('Error: %s' %(api_url_sev.status_code))

        for key in key_list:
            if key is not None:
                
                api_url_sev = requests.get("https://codi.qualitat.solucions.gencat.cat/api/measures/search?projectKeys=%s&metricKeys=duplicated_lines_density&ps=100" %(key), auth=HTTPBasicAuth(username, password))

                if api_url_sev.status_code == 200:
                    data = api_url_sev.json()
                    value = data['measures'][0]['value']
                    value = float(data['measures'][0]['value'])

                    """# duplicated code
                    if value > 0: value = 0.5
                    elif value == 0: value = 1
                    else: value = 0"""

                    with open('reports/duplicated_lines.txt', 'a') as f:
                        f.write(' %s: %s \r      ' %(key, value))
                else:
                    print('Error: %s' %(api_url_sev.status_code))

        for key in key_list:
            if key is not None:
                
                api_url_sev = requests.get("https://codi.qualitat.solucions.gencat.cat/api/measures/component?component=%s&metricKeys=security_rating&ps=100" %(key), auth=HTTPBasicAuth(username, password))

                if api_url_sev.status_code == 200:
                    data = api_url_sev.json()
                    measure = data['component']['measures'] # get the value of the metric
                    for value in measure:
                        measure = value['value'].replace('1.0', 'A').replace('2.0', 'B').replace('3.0', 'C').replace('4.0', 'D').replace('5.0', 'E') # replace the letter with a number

                        if measure == 'A':
                           measure = "100"
                        elif measure == 'B':
                            measure = "70"
                        elif measure == 'C':
                            measure = "40"
                        elif measure == 'D':
                            measure = "20"
                        elif measure == 'E':
                            measure = "0"

                    with open('reports/security-rating.txt', 'a') as f:
                        f.write(' %s: %s \r      ' %(key, measure))    
                else:
                    print('Error: %s' %(api_url_sev.status_code))

        for key in key_list:
            if key is not None:
                
                api_url_sev = requests.get("https://codi.qualitat.solucions.gencat.cat/api/issues/search?componentKeys=%s&types=VULNERABILITY&ps=100" %(key), auth=HTTPBasicAuth(username, password))

                if api_url_sev.status_code == 200:
                    data = api_url_sev.json()
                    total = data['total']
                    with open('reports/vulnerabilities.txt', 'a') as f:
                        f.write(' %s: %s \r      ' %(key, total))    
                else:
                    print('Error: %s' %(api_url_sev.status_code))

        for key in key_list:
            if key is not None:
                
                api_url_sev = requests.get("https://codi.qualitat.solucions.gencat.cat/api/issues/search?componentKeys=%s&types=VULNERABILITY&severities=BLOCKER&ps=100" %(key), auth=HTTPBasicAuth(username, password))

                if api_url_sev.status_code == 200:
                    data = api_url_sev.json()
                    total = data['total']
                    with open('reports/vulnerabilities-blocker.txt', 'a') as f:
                        f.write(' %s: %s \r      ' %(key, total))    
                else:
                    print('Error: %s' %(api_url_sev.status_code))

        for key in key_list:
            if key is not None:
                
                api_url_sev = requests.get("https://codi.qualitat.solucions.gencat.cat/api/issues/search?componentKeys=%s&types=VULNERABILITY&severities=CRITICAL&ps=100" %(key), auth=HTTPBasicAuth(username, password))

                if api_url_sev.status_code == 200:
                    data = api_url_sev.json()
                    total = data['total']
                    with open('reports/vulnerabilities-critical.txt', 'a') as f:
                        f.write(' %s: %s \r      ' %(key, total))    
                else:
                    print('Error: %s' %(api_url_sev.status_code))  

        for key in key_list:
            if key is not None:
                
                api_url_sev = requests.get("https://codi.qualitat.solucions.gencat.cat/api/issues/search?componentKeys=%s&types=CODE_SMELL,BUG,VULNERABILITY&severities=BLOCKER&ps=100" %(key), auth=HTTPBasicAuth(username, password))

                if api_url_sev.status_code == 200:
                    data = api_url_sev.json()
                    total = data['total']
                    with open('reports/total-severities-blocker.txt', 'a') as f:
                        f.write(' %s: %s \r      ' %(key, total))    
                else:
                    print('Error: %s' %(api_url_sev.status_code))   

        for key in key_list:
            if key is not None:
                
                api_url_sev = requests.get("https://codi.qualitat.solucions.gencat.cat/api/issues/search?componentKeys=%s&types=CODE_SMELL,BUG,VULNERABILITY&severities=CRITICAL&ps=100" %(key), auth=HTTPBasicAuth(username, password))

                if api_url_sev.status_code == 200:
                    data = api_url_sev.json()
                    total = data['total']
                    with open('reports/total-severities-critical.txt', 'a') as f:
                        f.write(' %s: %s \r      ' %(key, total))    
                else:
                    print('Error: %s' %(api_url_sev.status_code))
            
                        
    except Exception as error:
        print(error)
    
if __name__ == "__main__":

    get_values(request=None, key_list=['key'], sonar=None, total=['total'], measure=['measure'], value=['value'], ncloc=['ncloc'])