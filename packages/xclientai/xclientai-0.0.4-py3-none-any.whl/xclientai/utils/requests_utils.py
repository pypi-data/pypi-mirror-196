import requests
from requests.adapters import HTTPAdapter, Retry
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



def do_request(
    url, 
    http_method, 
    json_data=None, 
    headers=None
):
    session = requests.Session()
    retries = Retry(
        total=5,
        status_forcelist=[ 500, 502, 503, 504 ]
    )
    
    session.mount("http://", HTTPAdapter(max_retries=retries))
    
    params = {
        "url": url, 
        "json": json_data,
        "timeout": 300,
        "headers": headers,
        "verify": False
    }
    
    if http_method == "get":
        response = session.get(**params)
    elif http_method == "post":
        response = session.post(**params)
    elif http_method == "patch":
        response = session.patch(**params)
    elif http_method == "delete":
        response = session.delete(**params)
    elif http_method == "put":
        response = session.put(**params)
    
    try:
        response.raise_for_status()
    except Exception as ex:
        raise Exception(response.json()["message"])
    
    return response