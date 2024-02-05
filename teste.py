import pandas as pd
 
url = 'https://www.msn.com/en-au/sport/football/epl/ladder'
 
df_list = pd.read_html(url)
 
print(df_list[0])