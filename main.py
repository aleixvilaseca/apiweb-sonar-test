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


def get_severities(request, key_list, sonar, total): 
    
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

    key_list = str(key_list).replace('[', '').replace(']', '').replace("'", "").replace(" ", "").split(',') # remove the brackets from the list (not needed for the API

    try:
        for key in key_list:
            if key is not None:
                
                api_url_sev = requests.get("https://codi.qualitat.solucions.gencat.cat/api/issues/search?componentKeys=%s&types=VULNERABILITY&severities=BLOCKER,CRITICAL&ps=100" %(key), auth=HTTPBasicAuth(username, password))

                api_url_sev = api_url_sev.json()
                api_url_sev = api_url_sev['total']
                api_url_sev = str(api_url_sev)
                
                for total in api_url_sev:
                    if total is not None:
                        total = " ".join(key).replace(" ", ""), total.split(',')
                        total = str(total).replace('[', '').replace(']', '').replace("'", "").replace("(", " ").replace(")", " ").strip()

                        metric_file = open("reports/severity_list.json", "a")
                        metric_file.write(total)
                        metric_file.write("\n")
                        metric_file.close()
                        
    except Exception as error:
        print(error)
    
if __name__ == "__main__":

    get_severities(request=None, key_list=['key'], sonar=None, total=['total'])