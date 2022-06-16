# Sample lambda code that receives the input parameters through a gateway api and sends emails using aws ses

import json
import boto3
import logging

# Configure logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def lambda_handler(event, context):
    print("EVENT: ", event)
    params = event['queryStringParameters']
    param_keys = params.keys()

    to_address = params['to_address'].split(',')
    
    if 'cc_address' in param_keys:
        cc_address = params['cc_address'].split(',')
    else:
        cc_address = []
    
    if 'bcc_address' in param_keys:
        bcc_address = params['bcc_address'].split(',')
    else:
        bcc_address = []
        
    message = params['message']
    subject = params['subject']
    
    ses_client = boto3.client('ses')
    try:
        mail_response = ses_client.send_email(
            Destination={'BccAddresses': bcc_address,'CcAddresses': cc_address,'ToAddresses': to_address},   
            Message={'Body': {'Html': {'Charset': 'UTF-8','Data': message,}},'Subject': {'Charset': 'UTF-8','Data': subject,},},
            ReplyToAddresses=['abc@xyz.com'],      # Verified email in SES
            ReturnPath='abc@xyz.com',
            Source='John Smith <abc@xyz.com>'
        )
    except Exception as e:
        logger.error(e)
        return -1
    else:
        logger.info("Email sent! Message ID: {}".format(mail_response['MessageId']))
        return 
        # time.sleep(1)  # Delay to avoid throttling errors
