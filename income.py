from urllib.request import Request,urlopen
from bs4 import BeautifulSoup
import pandas as pd
import regex as re

req = Request(
    url = 'https://statusinvest.com.br/acoes/suzb3',
    headers={'User-Agent':'Firefox'}
)

html = urlopen(req)
soup = BeautifulSoup(html, 'html.parser')

header = soup.find('div',{'class':'table-info-body'})
table = header.find_next('table')

headers = []
for i in table.find_all('th'):
    title = i.text.strip()
    headers.append(title)
mydata = pd.DataFrame(columns = headers)

table_body=table.find('tbody')
rows = table_body.find_all('tr')

for row in rows:
    regex = re.compile('.*level-0.*')
    cols=row.find_all('td', attrs={"class" : regex })
    col=[x.text.strip() for x in cols]
    length = len(mydata)
    mydata.append = col
    print(col)

print(mydata)
