import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from windchill_client import WindchillClient

client = WindchillClient()
token = client.get_csrf_token()
print('CSRF Token:', token)