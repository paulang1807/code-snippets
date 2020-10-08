# Based on https://aws.amazon.com/blogs/database/using-the-data-api-to-interact-with-an-amazon-aurora-serverless-mysql-database/
import boto3
import datetime

# Helper function for executing the query
def execute_rds_query(host_arn, secret_arn, db_name, query, args, transactionId=None):
        params = {
            'secretArn': secret_arn,
            'includeResultMetadata': True,
            'database': db_name,
            'resourceArn': host_arn,
            'sql': query,
            'parameters': args
        }
        if transactionId is not None:
            params['transactionId'] = transactionId

        response = client.execute_statement(**params)

        return response

# Helper Function to format the rds response
def formatRecords(response):
    lstResponse = []   # List to store the final formatted response
    lstColNames = []   # List to store column names
    
    dictColNames = response['columnMetadata']  # Dictionary for column metadata part of the response
    dictColVals = response['records']   # Dictionary for query result part of the response
    
    # Extract the column names in a list
    for indx,coldict in enumerate(dictColNames):
        lstColNames.append(coldict['name'])
        
    for record in dictColVals:    # Loop through the resultset
        dictRecVals = {}

        # Loop through individual values in each record
        for indx,recVal in enumerate(record):  
            # Create a key value pair of column name and value and add to dictionary
            try: # Handle date object
                date_time_obj = datetime.datetime.strptime(str(list(recVal.values())[0]), '%Y-%m-%d %H:%M:%S')
                dictRecVals[lstColNames[indx]] = date_time_obj
            except ValueError:
                dictRecVals[lstColNames[indx]] = list(recVal.values())[0] 
        lstResponse.append(dictRecVals)
        
    return lstResponse

# arn for the rds cluster
host_arn='arn:aws:rds:us-west-2:123456789:cluster:cluster-name'  
# arn of the secret in secrets manager  
secret_arn='arn:aws:secretsmanager:us-west-2:123456789:secret:rds-db-credentials/cluster-6M4TLTDM4P2YVVU367F3N3G2OI/rdsuser-ABCDEF'
db_name="oip"     # database name

# Prepare query
argDt = "somedate"
arg1Val="someval"
argDt = datetime.datetime.strptime(argDt, '%Y-%m-%dT%H:%M:%S.%fZ')   # convert date to UTC date string
args = [{'name':'arg1', 'value':{'stringValue': f'{arg1Val}'}},
        {'name':'argDt', 'value':{'stringValue': f'{argDt}'}}]
query="select * from db.table where a=:arg1 and b=:argDt;"

client = boto3.client('rds-data')

# TRANSACTION BASED QUERY
# Get Transaction Id
transaction_id = client.begin_transaction(
                database=db_name,
                resourceArn=host_arn,
                secretArn=secret_arn
)

# Get response  and commit if successful, else rollback
try:
    response = execute_rds_query(host_arn, secret_arn, db_name, query, args, transaction_id['transactionId'])
    
    client.commit_transaction(
        resourceArn=host_arn,
        secretArn=secret_arn,
        transactionId=transaction_id['transactionId']
    )
except Exception as e:
    # I think this will only roll back the specifics users or lambada actions call
    client.rollback_transaction(
        resourceArn=host_arn,
        secretArn=secret_arn,
        transactionId=transaction_id['transactionId']
    )

# STANDALONE QUERY
response = execute_rds_query(host_arn, secret_arn, db_name, query, args)

# Get parsed resultset
finalResults = formatRecords(response)