import requests
import json
import csv
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


def get_values(request, key_list, sonar, ncloc, maintainability, duplicated, security_debt, reliability, technical_debt, security_rating, vulnerabilities, sblocker, scritical, blocker, critical): 

    print('Connection to Sonarqube')
    url = "https://codi.qualitat.solucions.gencat.cat/"

    with open('fixtures/config.json') as f:
        config = json.load(f)
    username = config['SONAR_USER']
    password = config['SONAR_PASSWORD']

    sonar = SonarQubeClient(url, username, password)

    print('Getting all projects')
    sonar = list(sonar.projects.search_projects()) # search all sonarqube projects
        
    key_list = []
    for key in sonar:
        key_list.append(key['key']) # append the project key to a list

    for key in range(len(key_list)):
        if key_list[key] == '0192-0206-tributs':
            key_list[key] = key_list[key].replace('0192-', '', 1)
        
    strings_to_remove = constants.APPLICATIONS_TO_EXCLUDE
    for string in strings_to_remove:
        if string in key_list:
            key_list.remove(string)

    key_list = str(key_list).replace('[', '').replace(']', '').replace("'", "").replace(" ", "").split(',') # remove the brackets from the list (not needed for the API
    
    try:

        print('Getting NCLOC')
        for key in key_list:
            if key is None or key == "":

                continue
                
            api_url_ncloc = requests.get(constants.GET_NCLOC_URL %(key), auth=HTTPBasicAuth(username, password))

            if api_url_ncloc.status_code == 200:
                data = api_url_ncloc.json()
                if data["component"]["measures"] == []:
                    ncloc = 0
                else:    
                    ncloc = data["component"]["measures"][0]["value"]
                    ncloc = int(ncloc)

            else:
                print('Error: %s: %s' %(key, api_url_ncloc.status_code))

        print('Getting Technical Debt')
        for key in key_list:
            if key is not None:
                
                api_url_maintainability = requests.get(constants.GET_MAINTAINABILITY_URL %(key), auth=HTTPBasicAuth(username, password))

                if api_url_maintainability.status_code == 200:
                    data = api_url_maintainability.json()
                    maintainability = data["component"]["measures"][0]["value"]

                    if maintainability == None:
                        maintainability = 0

                    maintainability = float(maintainability)

                api_url_reliability = requests.get(constants.GET_RELIABILITY_URL %(key), auth=HTTPBasicAuth(username, password))

                if api_url_reliability.status_code == 200:
                    data = api_url_reliability.json()
                    reliability = data["component"]["measures"][0]["value"]

                    if reliability == None:
                        reliability = 0

                    reliability = float(reliability)

                    if ncloc != 0:

                        reliability = reliability / 60 # convert minutes to hours
                        reliability = reliability / 8 # hours into working days
                    
                        reliability = (reliability / (ncloc * 0.06)) * 100

                technical_debt = (reliability + maintainability)
                technical_debt = ((100 - technical_debt) / 100)
                if technical_debt < 0: technical_debt = 0
                technical_debt = round(technical_debt, 2)

                with open('reports/technical_debt.txt', 'a') as f:
                    f.write(' %s: %s \r      ' %(key, technical_debt)) 

            else:
                print('Error: %s: %s' %(key, api_url_maintainability.status_code))


        print('Getting Technical Debt Security')
        for key in key_list:
            if key is not None:
                
                api_url_security = requests.get(constants.GET_SECURITY_EFFORT_URL %(key), auth=HTTPBasicAuth(username, password))

                if api_url_security.status_code == 200:
                    data = api_url_security.json()
                    security_debt = (data["measures"][0]["value"])
                    security_debt = int(security_debt)

                    if ncloc != 0:

                        security_debt = security_debt / 60 # convert minutes to hours
                        security_debt = security_debt / 8 # hours into working days
                    
                        security_debt = (security_debt / (ncloc * 0.06)) * 100

                        # technical debt security
                        security_debt = ((100 - security_debt) / 100)
                        if security_debt < 0: security_debt = 0
                        security_debt = round(security_debt, 2)

                with open('reports/technical_debt_sec.txt', 'a') as f:
                    f.write(' %s: %s \r      ' %(key, security_debt))    

            else:
                print('Error: %s: %s' %(key, api_url_security.status_code))

        print('Getting Duplicated Code')
        for key in key_list:
            if key is not None:
                
                api_url_duplicated = requests.get(constants.GET_DUPLICATED_LINES_URL %(key), auth=HTTPBasicAuth(username, password))

                if api_url_duplicated.status_code == 200:
                    data = api_url_duplicated.json()
                    if data["measures"] == []:
                        duplicated = 0
                    else:
                        duplicated = data['measures'][0]['value']
                        duplicated = float(data['measures'][0]['value'])
                        duplicated = round(duplicated, 2)

                    with open('reports/duplicated_lines.txt', 'a') as f:
                        f.write(' %s: %s \r      ' %(key, duplicated))
            else:
                print('Error: %s: %s' %(key, api_url_duplicated.status_code))

        print('Getting Security Rating')
        for key in key_list:
            if key is not None:
                
                api_url_sec_rating = requests.get(constants.GET_SECURITY_RATING_URL %(key), auth=HTTPBasicAuth(username, password))

                if api_url_sec_rating.status_code == 200:
                    data = api_url_sec_rating.json()
                    security_rating = data['component']['measures'] # get the value of the metric
                    for value in security_rating:
                        security_rating = value['value'].replace('1.0', 'A').replace('2.0', 'B').replace('3.0', 'C').replace('4.0', 'D').replace('5.0', 'E') # replace the letter with a number

                        if security_rating == 'A':
                           security_rating = "100"
                        elif security_rating == 'B':
                            security_rating = "70"
                        elif security_rating == 'C':
                            security_rating = "40"
                        elif security_rating == 'D':
                            security_rating = "20"
                        elif security_rating == 'E':
                            security_rating = "0"

                    with open('reports/security-rating.txt', 'a') as f:
                        f.write(' %s: %s \r      ' %(key, security_rating))    
            else:
                print('Error: %s: %s' %(key, api_url_sec_rating.status_code))

        print('Getting Vulnerabilities')
        for key in key_list:
            if key is not None:
                
                api_url_vulnerabilities = requests.get(constants.GET_VULNERABILITIES_URL %(key), auth=HTTPBasicAuth(username, password))

                if api_url_vulnerabilities.status_code == 200:
                    data = api_url_vulnerabilities.json()
                    vulnerabilities = int(data['total'])
                    with open('reports/vulnerabilities.txt', 'a') as f:
                        f.write(' %s: %s \r      ' %(key, vulnerabilities))    
            else:
                print('Error: %s: %s' %(key, api_url_vulnerabilities.status_code))

        print('Getting Security Blocker')
        for key in key_list:
            if key is not None:
                
                api_url_sblocker = requests.get(constants.GET_SECURITY_BLOCKER_URL %(key), auth=HTTPBasicAuth(username, password))

                if api_url_sblocker .status_code == 200:
                    data = api_url_sblocker .json()
                    sblocker = int(data['total'])
                    with open('reports/vulnerabilities-blocker.txt', 'a') as f:
                        f.write(' %s: %s \r      ' %(key, sblocker))    
            else:
                print('Error: %s: %s' %(key, api_url_sblocker.status_code))

        print('Getting Security Critical')
        for key in key_list:
            if key is not None:
                
                api_url_scritical = requests.get(constants.GET_SECURITY_CRITICAL_URL %(key), auth=HTTPBasicAuth(username, password))

                if api_url_scritical.status_code == 200:
                    data = api_url_scritical.json()
                    scritical = int(data['total'])
                    with open('reports/vulnerabilities-critical.txt', 'a') as f:
                        f.write(' %s: %s \r      ' %(key, scritical))    
            else:
                print('Error: %s: %s' %(key, api_url_scritical.status_code))  

        print('Getting Blocker')
        for key in key_list:
            if key is not None:
                
                api_url_blocker = requests.get(constants.GET_BLOCKER_URL %(key), auth=HTTPBasicAuth(username, password))

                if api_url_blocker.status_code == 200:
                    data = api_url_blocker.json()
                    blocker = int(data['total'])
                    with open('reports/total-severity-blocker.txt', 'a') as f:
                        f.write(' %s: %s \r      ' %(key, blocker))
                if blocker < sblocker: 
                    with open('reports/total-error-blocker.txt', 'a') as f:
                        f.write(' %s: %s \r      ' %(key, blocker))
            else:
                print('Error: %s: %s' %(key, api_url_blocker.status_code))   

        print('Getting Critical')
        for key in key_list:
            if key is not None:
                
                api_url_critical = requests.get(constants.GET_CRITICAL_URL %(key), auth=HTTPBasicAuth(username, password))

                if api_url_critical.status_code == 200:
                    data = api_url_critical.json()
                    critical = int(data['total'])
                    with open('reports/total-severity-critical.txt', 'a') as f:
                        f.write(' %s: %s \r      ' %(key, critical))
                if critical < scritical: 
                    with open('reports/total-error-critical.txt', 'a') as f:
                        f.write(' %s: %s \r      ' %(key, critical))
            else:
                print('Error: %s: %s' %(key, api_url_critical.status_code))
            
                        
    except Exception as error:
        print(error)
    
if __name__ == "__main__":

    get_values(request=None, key_list=['key'], sonar=None, ncloc=['ncloc'], maintainability=['maintainability'], duplicated=['duplicated'], security_debt=['security_debt'], reliability=['reliability'], technical_debt=['technical_debt'], security_rating=['security_rating'], vulnerabilities=['vulnerabilities'], sblocker=['sblocker'], scritical=['scritical'], blocker=['blocker'], critical=['critical'])