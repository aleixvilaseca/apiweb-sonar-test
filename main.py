import requests
from os.path import exists
import json
import sys
from openpyxl.workbook import workbook
import openpyxl
import os
import urllib3
import pyslurpers

# Get the data from SonarQube
"""username = 'admin'
password = 'CroLeveStM'

api_url_blocker = "https://codi.qualitat.solucions.gencat.cat/api/issues/search?componentKeys=0434-gsitgf&types=VULNERABILITY&severities=BLOCKER"

data_file = open("reports/blockers.json", "w") # write the security data to a file so we can use it later
data_file.write(json.dumps(api_url_blocker))
data_file.close()

api_url_critical = "https://codi.qualitat.solucions.gencat.cat/api/issues/search?componentKeys=0434-gsitgf&types=VULNERABILITY&severities=CRITICAL"

data_file = open("reports/criticals.json", "w") # write the security data to a file so we can use it later
data_file.write(json.dumps(api_url_critical))
data_file.close()"""

def sonarRest(url,method):
    username = 'admin'
    password = 'CroLeveStM'

    #api_url_blocker = "https://codi.qualitat.solucions.gencat.cat/api/issues/search?componentKeys=0434-gsitgf&types=VULNERABILITY&severities=BLOCKER"
    #api_url_critical = "https://codi.qualitat.solucions.gencat.cat/api/issues/search?componentKeys=0434-gsitgf&types=VULNERABILITY&severities=CRITICAL"

    api_url_blocker = sonarRest('https://codi.qualitat.solucions.gencat.cat/api/issues/search?types=VULNERABILITY&severities=BLOCKER', 'GET')
    total = (api_url_blocker.total.toFloat()/100).round()

    counter = 1

    while(counter <= total):
        api_url_blocker = sonarRest("https://codi.qualitat.solucions.gencat.cat/api/issues/search?types=VULNERABILITY&severities=BLOCKER", 'GET')
        print(api_url_blocker)
        counter+1

        data_file = open("reports/criticals.json", "w") # write the security data to a file so we can use it later
        data_file.write(json.dumps(api_url_blocker))
        data_file.close()
