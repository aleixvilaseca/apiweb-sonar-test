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


def get_severities(request, key_list, sonar): 

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

    metric_file = open("reports/project_list.json", "w") # write the security data to a file so we can use it later
    metric_file.write(json.dumps(key_list))
    metric_file.close()

    key_list = str(key_list).replace('[', '').replace(']', '').replace("'", "").replace(" ", "") # remove the brackets from the list (not needed for the API
    key_list = key_list.split(',') # split the list into a list of strings

    try:
        for key in key_list:
            if key is not None:
                api_url_sev = requests.get("https://codi.qualitat.solucions.gencat.cat/api/issues/search?componentKeys=%s&types=VULNERABILITY&severities=BLOCKER,CRITICAL" %(key), auth=HTTPBasicAuth(username, password))
                api_url_sev.json()

            """data_file = open("reports/severities1.json", "w") # write the security data to a file so we can use it later
            data_file.write(json.dumps(api_url_sev.json()))
            data_file.close()"""

    except Exception as error:
        print(error)

    """api_url_sev = list(api_url_sev)
    total = []
    for total in api_url_sev:
        total.append(total['total']), ",".join(total, key)"""

    


if __name__ == "__main__":

    get_severities(request=None, key_list=['key'], sonar=None)