import json
import requests

def lambda_handler(event, context):
    to_address = event['to_address']
    message = event['message']
    subject = event['subject']

    url = "https://<api_id>.execute-api.us-west-2.amazonaws.com/<api-stage>/<api-resource>"   # Invoke url for the api
    params = {'to_address': to_address, 'message': message, 'subject': subject}
    resp = requests.get(url, params=params)
    return resp.status_code