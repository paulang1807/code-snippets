import pandas as pd

filename="tst"

data_xls = pd.read_excel('{}.xls'.format(filename), 'Sheet1', index_col=None)
data_xls.to_csv('{}.csv'.format(filename), encoding='utf-8', index=False)