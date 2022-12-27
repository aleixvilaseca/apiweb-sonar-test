import requests

LONG_DEPARTMENTS = [
    "DEPT. DE LA VICEPRESIDÈNCIA I DE POL. DIG. I TERRITORI",
    "DEPT. D'ACCIÓ CLIMÀTICA, ALIMENTACIÓ I AGENDA RURAL",
    "DEPT. D'ACCIÓ EXTERIOR I GOVERN OBERT"
    ]

DEPARTMENTS_ORDER_LIST = [
        "DEPARTAMENT DE LA PRESIDÈNCIA",
        "DEPARTAMENT DE LA VICEPRESIDÈNCIA I DE POL. DIG. I TERRITORI",
        "DEPARTAMENT D'EMPRESA I TREBALL",
        "DEPARTAMENT D'ECONOMIA I HISENDA",
        "DEPARTAMENT D'IGUALTAT I FEMINISMES",
        "DEPARTAMENT D'ACCIÓ EXTERIOR I GOVERN OBERT",
        "DEPARTAMENT D'EDUCACIÓ",
        "DEPARTAMENT DE RECERCA I UNIVERSITATS",
        "DEPARTAMENT D'ACCIÓ CLIMÀTICA, ALIMENTACIÓ I AGENDA RURAL",
        "DEPARTAMENT DE SALUT",
        "DEPARTAMENT D'INTERIOR",
        "DEPARTAMENT DE DRETS SOCIALS",
        "DEPARTAMENT DE CULTURA",
        "DEPARTAMENT DE JUSTÍCIA"
    ]

def download_inventari():
    print('Downloading inventari')
    inventari = None
    try:
        response = requests.get('http://localhost:5000/inventari', timeout=5)
        if response.status_code == 200:
            inventari = response.json()
        else:
            print('Error downloading inventari. Please check connection with CTTI API')
    except requests.exceptions.ConnectionError:
        print('Error downloading inventari. Please check connection with CTTI API')

    return inventari

def get_departments_order():
    return DEPARTMENTS_ORDER_LIST

def truncate_department_if_long(department_name, type_of_trunc="<br>"):
    new_department_name = department_name
    if (department_name in LONG_DEPARTMENTS):
        if department_name == "DEPT. DE LA VICEPRESIDÈNCIA I DE POL. DIG. I TERRITORI":
            new_department_name = department_name.replace(" I DE POL. ", f"{type_of_trunc}DE POL. ")
        elif department_name == "DEPT. D'ACCIÓ CLIMÀTICA, ALIMENTACIÓ I AGENDA RURAL":
            new_department_name = department_name.replace(", A", f"{type_of_trunc}A")
        elif department_name == "DEPT. D'ACCIÓ EXTERIOR I GOVERN OBERT":
            new_department_name = department_name.replace(" I ", type_of_trunc)
    return new_department_name

def normalize_department_name(old_department):
    new_department = old_department

    if old_department in ["DEPARTAMENT DE PRESIDÈNCIA", "DEPARTAMENT DE LA PRESIDENCIA"]:
        new_department = DEPARTMENTS_ORDER_LIST[0]

    if old_department in ["DEPARTAMENT DE VICEPRESIDÈNCIA I DE POLÍTIQUES DIGITALS I TERRITORI"]:
        new_department = DEPARTMENTS_ORDER_LIST[1]

    return new_department