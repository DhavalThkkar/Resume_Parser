# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 18:06:38 2021

@author: MSI
"""

import requests
import json
import numpy as np
import pandas as pd
from pandas import json_normalize

auth_endpoint = "https://auth.emsicloud.com/connect/token" # auth endpoint

client_id = "f0l2nqmdb7jb37u4"
client_secret = "cj02e2qJ"
scope = "emsi_open"

payload = "client_id=" + client_id + "&client_secret=" + client_secret + "&grant_type=client_credentials&scope=" + scope # set credentials and scope
headers = {'content-type': 'application/x-www-form-urlencoded'} # headers for the response
access_token = json.loads((requests.request("POST", auth_endpoint, data=payload, headers=headers)).text)['access_token']

def extract_skills_list():
  all_skills_endpoint = "https://emsiservices.com/skills/versions/latest/skills" # List of all skills endpoint
  auth = "Authorization: Bearer " + access_token # Auth string including access token from above
  headers = {'authorization': auth} # headers
  response = requests.request("GET", all_skills_endpoint, headers=headers) # response
  response = response.json()['data'] # the data

  all_skills_df = pd.DataFrame(json_normalize(response)); # Where response is a JSON object drilled down to the level of 'data' key
  return all_skills_df

a = extract_skills_list()