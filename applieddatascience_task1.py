##Importing libraries

from bs4 import BeautifulSoup
import requests
import pandas as pd

# download url data from internet
url = "https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M"
source = requests.get(url).text
Canada_data = BeautifulSoup(source, 'lxml')

## ##Convert HTML table with postal codes as dataframe
## Create new dataframe

column_names = ['Postalcode','Borough','Neighborhood']
toronto = pd.DataFrame(columns = column_names)

# loop through to find postcode, borough and neighborhood 
content = Canada_data.find('div', class_='mw-parser-output')
table = content.table.tbody
postcode = 0
borough = 0
neighborhood = 0

for tr in table.find_all('tr'):
    k = 0
    for td in tr.find_all('td'):
        if k == 0:
            postcode = td.text
            k = k + 1
        elif k == 1:
            borough = td.text
            k = k + 1
        elif k == 2: 
            neighborhood = td.text.strip('\n').replace(']','')
    toronto = toronto.append({'Postalcode': postcode,'Borough': borough,'Neighborhood': neighborhood},ignore_index=True)

# clean dataframe

# The approach followed when more than one neighborhood can exist in one postal code area,
# these rows will be combined into one row with the neighborhoods separated with a comma

# If a cell has a borough but a Not assigned neighborhood, then the neighborhood will be the same as the borough

toronto = toronto[toronto.Borough!='Not assigned']
toronto = toronto[toronto.Borough!= 0]
toronto.reset_index(drop = True, inplace = True)
k = 0
for k in range(0,toronto.shape[0]):
    if toronto.iloc[k][2] == 'Not assigned':
        toronto.iloc[k][2] = toronto.iloc[k][1]
        k = k+1
        df = toronto.groupby(['Postalcode','Borough'])['Neighborhood'].apply(', '.join).reset_index()
df.head(50)


## Data cleaning
## Ignore cells with a borough that is Not assigned

df = df.dropna()
Nan = 'Not assigned'
df = df[(df.Borough != Nan )]


df.head()


def neighborhood_list(grouped):    
    return ', '.join(sorted(grouped['Neighborhood'].tolist()))
                    
grp = df.groupby(['Postalcode', 'Borough'])
df1 = grp.apply(neighborhood_list).reset_index(name='Neighborhood')

print(df1.shape)
print(df1)