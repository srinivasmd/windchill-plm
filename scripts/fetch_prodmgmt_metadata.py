"""Fetch ProdMgmt metadata from Windchill"""
import requests
from requests.auth import HTTPBasicAuth

# Windchill configuration
BASE_URL = "https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/ProdMgmt"
AUTH = HTTPBasicAuth("pat", "ptc")

# Fetch metadata
response = requests.get(f"{BASE_URL}/$metadata", auth=AUTH, verify=False)

if response.status_code == 200:
    print(response.text)
else:
    print(f"Error: {response.status_code}")
    print(response.text)