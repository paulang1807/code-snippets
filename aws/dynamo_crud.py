
# CRUD examples for Dynamo DB

import json
import io
import argparse
import ast
import boto3
from botocore.exceptions import ClientError

class dynamoDB:
   
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        self.table = None
    def setTableName(self, tableName):
        table = self.dynamodb.Table(tableName)
        return table
    
    def scanFullTable(self, tableName):
        scanResponse = tableName.scan()
        return scanResponse
    
    def scanFiltered(self, tableName, lstDictFilter):
        """
        Base function to scan table filtered by the key value pairs of column names and values passed as parameter
        The column names can be both partition and sort keys as well as any other column in the table
        NOTE: If the total number of scanned items exceeds the maximum dataset size limit of 1 MB, 
        the scan stops and results are returned to the user as a LastEvaluatedKey value to continue 
        the scan in a subsequent operation
        """

        expFil=""
        expAttrVals={}
        expAttrCols={}
        counter=0

        for idx,dictFil in enumerate(lstDictFilter):
          tmpExpFil="("
          filters = ast.literal_eval(dictFil)

          for key,val in filters.items():
              counter += 1

              # Add filter expression separated by AND condition
              tmpExpFil += "#col{0} = :val{0}".format(counter) + " AND "

              # TIP: To use 'contains' filter expression instead of '=', the syntax will be 
              # tmpExpFil += "contains(#col, :val)"

              # Derive attribute names and values
              expAttrCols['#col{}'.format(counter)] = key
              expAttrVals[':val{}'.format(counter)] = val

          # Remove the 'AND' at end of the filter expression
          tmpExpFil = tmpExpFil.rstrip(" AND ")
          tmpExpFil += ")"
          expFil += tmpExpFil + " OR "

        # Remove the 'OR' at end of the filter expression
        expFil = expFil.rstrip(" OR ")

        queryParams={
            "FilterExpression": expFil,
            "ExpressionAttributeNames": {"#metricId": "metricId"},
            "ExpressionAttributeValues": expAttrVals
        }

        while True:
            if lastEvalKey is not None:
                queryParams["ExclusiveStartKey"] = lastEvalKey
            scanResponse = tableName.scan(**queryParams)
            print("SCAN RESP: ", len(scanResponse['Items']), scanResponse)
            if len(scanResponse['Items']) == 0 and 'LastEvaluatedKey' in scanResponse:
                lastEvalKey = scanResponse['LastEvaluatedKey']
            else:
                break
        return scanResponse
    
    def queryTable(self, tableName, dictKeys, dictFil=None):
        """
        Function to query table with just partition key or both partition and sort keys
        In case additional filters need to be applied, they can be passed using the dictFil parameter
        """

        keyCondExp=""
        filCondExp=""
        expAttrVals={}
        expAttrCols={}
        counter=0

        # Key Condition
        keyCols = ast.literal_eval(dictKeys)
        for key,val in keyCols.items():
          counter += 1

          # Add key condition separated by AND condition
          keyCondExp += "#idcol{0} = :idval{0}".format(counter) + " AND "

          # Derive attribute names and values
          expAttrCols['#idcol{}'.format(counter)] = key
          expAttrVals[':idval{}'.format(counter)] = val

        # Remove the 'AND' at end of the key condition
        keyCondExp = keyCondExp.rstrip(" AND ")

        if dictFil is not None:
          counter=0

          # Filter Condition
          filters = ast.literal_eval(dictFil)

          for key,val in filters.items():
            counter += 1

            # Add key condition separated by AND condition
            filCondExp += "#filcol{0} = :filval{0}".format(counter) + " AND "

            # Derive attribute names and values
            expAttrCols['#filcol{}'.format(counter)] = key
            expAttrVals[':filval{}'.format(counter)] = val

          # Remove the 'AND' at end of the key condition
          filCondExp = filCondExp.rstrip(" AND ")

          # Query Table
          qryResponse = tableName.query(
          KeyConditionExpression = keyCondExp,
          FilterExpression = filCondExp,
          ExpressionAttributeNames = expAttrCols,
          ExpressionAttributeValues = expAttrVals)
        else:
          # Query Table
          qryResponse = tableName.query(
          KeyConditionExpression = keyCondExp,
          ExpressionAttributeNames = expAttrCols,
          ExpressionAttributeValues = expAttrVals)

        return qryResponse
    
    def insertItemData(self, tableName, tableData):
        """
        Base function for inserting items in a table
        """

        try:
            for item in tableData:
                tableName.put_item(Item=item)
        except Exception as e:
            print(e.response['Error']['Message'])
            
    def removeItems(self, tableName, lstKeyCols=None, lstKey=None):
        """
        Base function for deleting items from a table
        If lstKey is not specified, lstKeyCols needs to be specified. The entire table is truncated based on the key column names
        If lstKey is specified, lstKeyCols does not need to be specified. Only the corresponding rows are deleted
        """

        if lstKey is None:      # Truncate table
            tableData = self.scanFullTable(tableName)       
            print("Truncating table ...")
            for item in tableData['Items']:
                key = {}
                for keyName in lstKeyCols:
                    key[keyName] = item[keyName]
                tableName.delete_item(Key=key)

        else:                   # Delete only specified keys
            print("Deleting specified keys ...")
            for keyVal in lstKey:
                key = ast.literal_eval(keyVal)
                tableName.delete_item(Key=key)
                
    def updateItem(self, tableName, item, lstKeyCols, colNm, colVal):
        """
        Base function for table update
        This example updates the data and the schema attributes
        The values for the key and attributes are passed in the form of a dictionary: 
        item={"idVal":"idval","data":"dataval", "schema":"schemaval"}
        """

        # Create Key dict
        key = {}
        for keyName in lstKeyCols:
            key[keyName] = item[keyName]

        # Parameters
        expUpd="set #colNm = :colVal"
        expAttrNames={"#colNm": colNm}
        expAttrVals={
            ':colVal': colVal
        }
        retVal="UPDATED_NEW"

        # Update Table
        updResponse = tableName.update_item(
          Key=key,
          ExpressionAttributeNames=expAttrNames,
          UpdateExpression=expUpd,
          ExpressionAttributeValues=expAttrVals,
          ReturnValues=retVal
        )
        
        return updResponse
        
    def appendItem(self, tableName, s3bkt, s3key):
        """
        Function for inserting new rows without truncating the table
        The data to be inserted is assumed to be in json format and stored in s3. 
        The s3 bucket and key are passed as parameters.
        """

        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket=s3bkt, Key=s3key)
        tableData = json.load(io.BytesIO(obj['Body'].read()))
        self.insertItemData(tableName, tableData)
    
    def insertItems(self, tableName, lstKeyCols, s3bkt, s3key):
        """
        Base function to truncate and load tables
        """

        self.removeItems(tableName, lstKeyCols=lstKeyCols)
        self.appendItem(tableName, s3bkt, s3key)

if __name__=='__main__':
    # Parse Variables : code not included
    
    try:
        apDynamo = dynamoDB()   
        tableName = apDynamo.setTableName("tblName") 

        # SCAN BY FILTERS 
        # Sample Calls:
        #   python testcrud.py --tableName "tblName" --lstDictFilter "{'partitionKeyName':'partitionKeyVal','sortKeyName':'sortKeyVal'}"
        #   python testcrud.py --tableName "tblName" --lstDictFilter "{'partitionKeyName':'partitionKeyVal1','filterColName':'filterColVal1'};{'partitionKeyName':'partitionKeyVal2','filterColName':'filterColVal2'}"
        #   NOTE: Use appropriate argument parse logic to parse the list parameters into lists
        # Function Call:
        #   apDynamo.scanFiltered(tableName, lstDictFilter)

        # QUERY TABLE
        # Sample Calls:
        #   python testcrud.py  --tableName "tblName" --dictKeys "{'partitionKeyName':'partitionKeyVal','sortKeyName':'sortKeyVal'}"
        #   python testcrud.py  --tableName "tblName" --dictKeys "{'partitionKeyName':'partitionKeyVal','sortKeyName':'sortKeyVal'}" --dictFil "{'filterCol1Name':'filterCol1Val','filterCol2Name':'filterCol2Val'}"
        # Function Calls:
        #   apDynamo.queryTable(tableName, dictKeys)
        #   apDynamo.queryTable(tableName, dictKeys, dictFil)

        # TRUNCATE AND LOAD 
        # Sample Calls:
        #   python testcrud.py --tableName "tblName" --keycols "partitionKeyColName" --s3bkt "bucket_name" --s3key "s3 key"
        #   python testcrud.py --tableName "tblName" --keycols "partitionKeyColName,sortKeyColName" --s3bkt "bucket_name" --s3key "s3 key"
        # Function Calls:
        #   apDynamo.insertItems(tableName, keycols, s3bkt, s3key)

        # APPEND ROWS TO TABLE
        # Sample Calls:
        #   python testcrud.py --tableName "tblName" --s3bkt "bucket_name" --s3key "s3 key"
        # Function Calls:
        #   apDynamo.appendItem(tableName, s3bkt, s3key)

        # DELETE SPECIFIED KEYS
        # Sample Calls:
        #   python testcrud.py --tableName "tblName" --lstId "{'partitionKeyName':'partitionKeyVal1'},{'partitionKeyName':'partitionKeyVal2'}"
        #   python testcrud.py --tableName "tblName" --lstId "{'partitionKeyName':'partitionKeyVal1','sortKeyName':'sortKeyVal1'},{'partitionKeyName':'partitionKeyVal2','sortKeyName':'sortKeyVal2'}"
        # Function Calls:
        #   apDynamo.removeItems(tableName, lstKey=lstId)

        # TRUNCATE TABLE
        # Sample Calls:
        #   python testcrud.py --tableName "tblName" --keycols "partitionKeyColName" 
        #   python testcrud.py --tableName "tblName" --keycols "partitionKeyColName,sortKeyColName" 
        # Function Calls:
        #   apDynamo.removeItems(tableName, lstKeyCols=keycols)

        # UPDATE ITEM IN TABLE
        # Update the 'fiscalYear' attribute for a specified set of ids, if specified, else the entire table
        # Sample Calls:
        #   python testcrud.py --tableName "tblName" --lstDictFilter "{'partitionKeyName':'partitionKeyVal','sortKeyName':'sortKeyVal'} --keycols "partitionKeyColName,sortKeyColName" --colNm "name_of_co_to_update" --colVal "value_to_use_for_update"
        #   python testcrud.py --tableName "tblName" --keycols "partitionKeyColName,sortKeyColName" --colNm "name_of_co_to_update" --colVal "value_to_use_for_update"
        # Function Calls:
        #   if lstDictFilter is not None:
        #       tableData = apDynamo.scanFiltered(tableName, lstDictFilter)
        #   else:
        #       tableData = apDynamo.scanFullTable(tableName)
        #   for item in tableData['Items']:
        #       apDynamo.updateItem(tableName, item, keycols, colNm, colVal)
        
    except ClientError as e:
        print(e.response['Error']['Message'])
