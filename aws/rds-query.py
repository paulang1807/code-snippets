import boto3

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
            dictRecVals[lstColNames[indx]] = list(recVal.values())[0]   
        lstResponse.append(dictRecVals)
        
    return lstResponse

# arn for the rds cluster
resource_arn='arn:aws:rds:us-west-2:123456789:cluster:cluster-name'  
# arn of the secret in secrets manager  
secret_arn='arn:aws:secretsmanager:us-west-2:123456789:secret:rds-db-credentials/cluster-6M4TLTDM4P2YVVU367F3N3G2OI/rdsuser-ABCDEF'
db_name="oip"     # database name

sql="select * from db.table where a=b;"

client = boto3.client('rds-data')

# Query the rds
response = client.execute_statement(
    database=db_name,
    includeResultMetadata=True,    # used to get the column names
    resourceArn=resource_arn,
    secretArn=secret_arn,
    sql=sql
)

finalResults = formatRecords(response)