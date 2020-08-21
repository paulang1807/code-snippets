""" 
Snippet to read csv files from url into df
"""

import pandas as pd
import io
import requests

url = "https://raw.githubusercontent.com/fivethirtyeight/data/master/avengers/avengers.csv"
csv_content=requests.get(url).content
df=pd.read_csv(io.StringIO(csv_content.decode('latin_1')))  # Use the appropriate encoding - utf-8, utf-16, latin_1 etc.
df.head()


# Without using dataframes
response = requests.get(url)
with open("./test.csv", "wb") as f:
    f.write(response.content)