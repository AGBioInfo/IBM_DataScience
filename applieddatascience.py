# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 14:31:56 2019

@author: Xpertnoob
"""

from bs4 import BeautifulSoup
import requests
import csv
import json
import xml
import pandas as pd

url='https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'
source = requests.get(url).text

soup = BeautifulSoup(source, 'lxml')#Beautiful Soup to Parse the url page

table=soup.find('table') #Finds the required table area

#List initialization to collect the Postalcodes, Boroughs and Neighborhoods
postalcode=[]
borough=[]
neighborhood=[]

x=table.tbody #Navidation to the body of the table

for tr in x.find_all('tr'): #Iterating through rows and columns
    td=tr.find_all('td')
    for x in td:
        #Exception handling to bypass the errors
        try:
            if x.span.text!='Not assigned':
                postalcode.append(x.b.text) #Collecting the Postalcodes
        except:
            pass
        try:
            if x.span.text!='Not assigned': 
                my=x.span.get_text(separator=u' ').split(' ')
                
                if my[1]=='York':
                    my_b= my[0]+' '+my[1]
                    borough.append(my_b)
                    my_nei=my[2:]
                    if my_nei==['\n'] or my_nei==[]:
                        neighborhood.append(my_b)
                    else:
                        my_nei1=' '.join(my_nei)
                        neighborhood.append(my_nei1.replace('(',',',5).replace(')',',',5).replace('/',',',5).strip(', '))
                
                elif my[1]=='Toronto':
                    my_b=my[0]+' '+my[1]
                    borough.append(my_b)
                    my_nei=my[2:]
                    if my_nei==['\n'] or my_nei==[]:
                        neighborhood.append(my_b)
                    else:
                        my_nei1=' '.join(my_nei)
                        neighborhood.append(my_nei1.replace('(',',',5).replace(')',',',5).replace('/',',',5).strip(', '))
                
                elif my[1]=='Park':
                    my_b=my[0]+' '+my[1]
                    borough.append(my_b)
                    my_nei=my[2:]
                    if my_nei==['\n'] or my_nei==[]:
                        neighborhood.append(my_b)
                    else:
                        my_nei1=' '.join(my_nei)
                        neighborhood.append(my_nei1.replace('(',',',5).replace(')',',',5).replace('/',',',5).strip(', '))
                
                else:
                    my_b=my[0]
                    borough.append(my_b)
                    my_nei=my[2:]
                    if my_nei==['\n'] or my_nei==[]:
                        neighborhood.append(my_b)
                    else:
                        my_nei1=' '.join(my_nei)
                        neighborhood.append(my_nei1.replace('(',',',5).replace(')',',',5).replace('/',',',5).strip(', '))
        except :
            pass


#Constructing the main dataframe 
main_df=pd.DataFrame({'PostalCode':postalcode,
                 'Borough':borough,
                 'Neighborhood':neighborhood})

    #Fixing the order of the columns in the main dataframe
main_df=main_df[['PostalCode','Borough','Neighborhood']]

#Visualizing the first few rows of the dataframe
main_df.head(10)

latitude=[] #List to collect the latitudes
longitude=[] #List to collect the longitudes

for i in main_df['PostalCode']: #Iterating through Postalcodes to collect the locations data
    try:
        j='toronto,'+i
        url ="https://maps.googleapis.com/maps/api/geocode/json?key={}&address={}".format(API_key,j)
        response = requests.get(url).json() # get response
        geographical_data = response['results'][0]['geometry']['location'] # get geographical coordinates
        latitude.append(geographical_data['lat'])
        longitude.append(geographical_data['lng'])
    except:
        pass
main_df['Latitude']=latitude #Adding a column in the main dataframe for Latitude  

main_df['Longitude']=longitude #Adding a column in the main dataframe for Longitude 
main_df.head()

main_df.Borough.unique()

print('The dataframe has {} boroughs and {} neighborhoods.'.format(
        len(main_df['Borough'].unique()),
      main_df.shape[0]
    )
)