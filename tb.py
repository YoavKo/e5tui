import pandas as pd
from tabulate import tabulate as tb 

df = pd.read_html('11.html')
print(type(df))
#print(df.valuse.tolist())
print(tb(df[0], headers='keys', tablefmt='psql'))
