
# Code snippet for triggering qlik tasks using the qrs api
# Blog Reference: https://community.qlik.com/t5/Integration-Extension-APIs/Executing-a-QlikSense-Task-using-the-QRS-API-with-Python/td-p/1838761
# API Reference:
# Reload: https://help.qlik.com/en-US/sense-developer/November2018/APIs/repositoryserviceapi/index.html?page=1048
# Get Status: https://help.qlik.com/en-US/sense-developer/November2018/APIs/repositoryserviceapi/index.html?page=597

import sys
import random
import string
import json
import requests
from urllib import parse
import boto3

# Variables
task_name = sys.argv[1]

# Get Auth Token
client = boto3.client(service_name='secretsmanager',region_name='us-west-2')
response = client.get_secret_value(SecretId='secret_name')
response_string = response['SecretString']
response_json = json.loads(response_string)
auth_token = response_json ["token"]

# Random Cross Site Forgery key
# See https://help.qlik.com/en-US/sense-developer/August2021/Subsystems/RepositoryServiceAPI/Content/Sense_RepositoryServiceAPI/RepositoryServiceAPI-Connect-API-Using-Xrfkey-Headers.htm
xrfkey = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=16))

headers = {"Authorization": auth_token, "X-Qlik-Xrfkey": xrfkey, "Content-Length": "0"}

qrs_reload_url = "https://<qliksense server url>/platformjwt/qrs/task/start/synchronous"
qrs_status_url = "https://<qliksense server url>/platformjwt/qrs/task"

qrs_trigger_task_url = qrs_reload_url + "?name=" + parse.quote(task_name) + "&xrfkey=" + xrfkey

status_filter = "name eq '" + task_name + "'"
qrs_task_status_url = qrs_status_url + "?xrfkey=" + xrfkey + "&filter=" + parse.quote(status_filter)

status_dict = {0: "NeverStarted", 1: "Triggered", 2: "Started", 3: "Queued", 4: "AbortInitiated", 5: "Aborting", 6: "Aborted", 7: "FinishedSuccess", 8: "FinishedFail", 9: "Skipped", 10: "Retry", 11: "Error", 12: "Reset"}

# Reload Task
trigger_resp = requests.post(qrs_trigger_task_url, headers=headers)
trigger_resp_json = trigger_resp.json()
print("Task reload response: ",trigger_resp_json)

# Get reload status
status_resp = requests.get(qrs_task_status_url, headers=headers)
status_resp_json = status_resp.json()
reload_status = status_resp_json[0]['operational']['lastExecutionResult']['status']
print("Task status is: ", status_dict[reload_status])

if reload_status not in [1,2,3,7]:
  sys.exit(1)