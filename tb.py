import pandas as pd
from tabulate import tabulate as tb 

dfs = pd.read_html('11.html')
data = dfs[0]
print(tb(data, headers='keys', tablefmt='psql'))
