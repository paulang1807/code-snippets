""" 
Snippets to query, insert and update records in quickbase
All snippets expect a user token and application token to be available
"""

import requests
import os
import io
import pandas as pd
import xml.etree.ElementTree as et

#  Id of the quickbase table. Can be retrieved from the quickbase url for the table
dbID = 'dbID'
userToken = 'userToken'
appToken = 'appToken'

# Query a table
# clist is a list of quickbase field ids
metricQry= "https://domain.quickbase.com/db/{0}?a=API_GenResultsTable&".format(dbID)
metricQry += "usertoken={}&apptoken={}}&".format(userToken, appToken) \
            "clist=6.144.146&slist=6&options=csv"
response=requests.get(metricQry).content
df1=pd.read_csv(io.StringIO(response.decode('ISO-8859-1')))

# Insert records in a table
# Using a dummy dataframe here. This should be replaced with the dataframe containing data
df = pd.DataFrame()  
for indx, row in df.iterrows():
    valToInsert = row['colName']
    metricQry= "https://domain.quickbase.com/db/{}?a=API_AddRecord&".format(dbID)
    metricQry += "usertoken={}&apptoken={}}&".format(userToken, appToken) \
                    "_fid_6={}".format(valToInsert)
    requests.get(metricQry).content

# Query table so that resultset includes record id and update id
# The update id is used to update the records
filter1='filter1'
filter2='filter2'

metricQry= "https://domain.quickbase.com/db/{0}?a=API_DoQuery&includeRids=1&".format(dbID)
metricQry += "usertoken={}&apptoken={}}&".format(userToken, appToken) \
            "query={'22'.CT." + str(filter1) + "}AND{'38'.CT." + filter2 + "}&clist=148&slist=3"
response=requests.get(metricQry).content

# Extract record id and update id from the resultset
xtree = et.XML(response)
for child in list(xtree):
    if child.tag == 'record':
        rec_id = child.attrib.get(key)
        update_id = child.find('update_id').text

# Update a table by field id
updVal='updVal'
metricQry= "https://domain.quickbase.com/db/{0}?a=API_EditRecord&rid={1}&".format(dbID, rec_id)
metricQry += "usertoken={}&apptoken={}}&".format(userToken, appToken) \
            "_fid_14={}&update_id={}".format(updVal, update_id)
requests.get(metricQry).content