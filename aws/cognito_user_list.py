# Function to get a given set of attributes for all cognito users
import boto3
import datetime
import json
import pandas as pd

REGION = 'us-west-2'
USER_POOL_ID = 'specify_user_pool_id_here'

client = boto3.client('cognito-idp', REGION)

pagination_token = None
page_count = 1
users_all = []

def get_cognito_users_list(cognito_idp_client, next_pagination_token = None):
    if next_pagination_token:
        return cognito_idp_client.list_users(
            UserPoolId = USER_POOL_ID,
            PaginationToken = next_pagination_token
        )
    else:
        return cognito_idp_client.list_users(
            UserPoolId = USER_POOL_ID)

while page_count ==1 or pagination_token is not None:
    user_records = get_cognito_users_list(
        cognito_idp_client = client,
        next_pagination_token = pagination_token)
    if "PaginationToken" in user_records.keys():
        pagination_token = user_records["PaginationToken"]
    else:
        pagination_token = None
    page_count += 1
    users = user_records['Users']
    users_all += users

df = pd.json_normalize(users_all, 'Attributes', ['Username','UserCreateDate','UserLastModifiedDate','Enabled','UserStatus'])
df1 = df[df.Name.isin(["custom:UserID","given_name","family_name","email"])]
df2 = df1.pivot(index='Username', columns='Name', values='Value')
df2.reset_index(inplace=True)
df2.columns=['cognito_username','user_id','email','family_name','give_name']