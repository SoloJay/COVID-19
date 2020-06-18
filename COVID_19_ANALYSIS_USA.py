#!/usr/bin/env python
# coding: utf-8

# In[1]:


#IMPORTING ALL RELEVANT MODELS 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from datetime import datetime
import geopandas as gpd
import pysal
from shapely.geometry import Point
import contextily as ctx


# source: https://data.world/associatedpress/johns-hopkins-coronavirus-case-tracker

# In[2]:


#import module
import datadotworld  as dw


# In[3]:


#read file online
cvd_data = dw.load_dataset('https://data.world/associatedpress/johns-hopkins-coronavirus-case-tracker',auto_update=True)


# In[4]:


#checking contents
cvd_data.describe()


# In[5]:


#Creating dataframe
USA_covid_19 = cvd_data.dataframes['1_county_level_confirmed_cases'] 
#check dataypes and columns
print(USA_covid_19.info())
#see some outputs
print(USA_covid_19.head())


# In[6]:


#for spatial analysis we select relevant columns
USA_covid_19 = USA_covid_19.loc[:,['state','county_name','lat','lon','total_population','confirmed','deaths']]


# In[7]:


#see output
print(USA_covid_19.head(3))


# In[8]:


#check missing values
print(USA_covid_19.isnull().sum())


# In[9]:


#fill missing values with zeros
USA_covid_19 = USA_covid_19.fillna(0)


# In[10]:


print(USA_covid_19.isnull().sum())


# In[11]:


#creating new column to store geometry points of coordinates using shapely points
USA_covid_19['geometry'] = [Point(xy) for xy in zip(USA_covid_19['lon'].astype('float'),USA_covid_19['lat'].astype('float'))]


# In[12]:


print(USA_covid_19.head())


# In[13]:


#dropping latitude and longitude columns as they are now stored in geometry column
USA_covid_19 = USA_covid_19.drop(['lon', 'lat'], axis=1)


# In[14]:


print(USA_covid_19.head())


# In[15]:


#assiging coordinate reference system to coordinate points of the geometry created above
USA_covid_19_point = gpd.GeoDataFrame(USA_covid_19,crs='epsg:4269')


# In[16]:


#read shape file
state_shp = gpd.read_file('./states_21basic/states.shp')


# In[17]:


#setting the same coordinate system as london ward. This ensures the points in the datasets aligns with the points
#in the shapefile, so that the locations are pinned properly on the map
USA_covid_19_point = USA_covid_19_point.to_crs(state_shp.crs)


# In[18]:


#spatial join of shapefile and acorn data
USA_covid_19_join = gpd.sjoin(USA_covid_19_point, state_shp, how="inner", op='intersects')


# In[19]:


#see output
print(USA_covid_19_join.head())


# In[20]:


#group states
confirmed = pd.DataFrame(USA_covid_19_join[['state', 'index_right',
                         'confirmed']].groupby('index_right')['confirmed'].sum())
deaths = pd.DataFrame(USA_covid_19_join[['state', 'index_right',
                         'deaths']].groupby('index_right')['deaths'].sum())


# In[21]:


# merging data with US state ward shapefile and filling any null entries with zeros.
confirmed_merged = state_shp.merge(confirmed, left_index = True, right_index = True, how = 'inner').fillna(0).reset_index()
deaths_merged = state_shp.merge(deaths, left_index = True, right_index = True, how = 'inner').fillna(0).reset_index()


# In[ ]:





# In[22]:


confirmed_merged= confirmed_merged[(confirmed_merged.STATE_NAME!='Hawaii') & (confirmed_merged.STATE_ABBR!='AK')]


# In[23]:


deaths_merged= deaths_merged[(deaths_merged.STATE_NAME!='Hawaii') & (deaths_merged.STATE_ABBR!='AK')]


# In[24]:





# In[ ]:





# In[25]:


#create a function to output last update of data
def last_update():
    cvd_data1 = dw.load_dataset('https://data.world/associatedpress/johns-hopkins-coronavirus-case-tracker',auto_update=True)
    cvd_data1 = cvd_data1.dataframes['1_county_level_confirmed_cases'] 
    cvd_data1['date'] = pd.to_datetime(cvd_data1['last_update'])
    date=cvd_data1.date[0].strftime('%B %d, %Y')
    return date


# In[26]:



#setting font scale to increase the legend size as they appeared tiny
print(sns.set(font_scale=1.8))

fig, ax = plt.subplots(1,1,figsize = (20,15))
print(ax.set_aspect('equal'))
print(confirmed_merged.plot(column = 'confirmed',
                          legend = True , k = 9, alpha=0.8, ax=ax,cmap='YlOrRd',
                       legend_kwds={'label': "\nTotal Cases",'orientation': "horizontal"}))
print(ctx.add_basemap(ax,zoom=12))
print(plt.title('\nConfirmed Cases Excluding Alaska and Hawaii (Last Update: {})'.format(last_update()), fontsize=25))
print(plt.axis('off'))
print(plt.tight_layout())
#creating new columns to store coordinate points to pick up name of each ward to label map
confirmed_merged['coords'] = confirmed_merged['geometry'].apply(lambda x: x.representative_point().coords[:])
confirmed_merged['coords'] = [coords[0] for coords in confirmed_merged['coords']]
for idx, row in confirmed_merged.iterrows():
    plt.annotate(s=row['STATE_ABBR'], xy=row['coords'],horizontalalignment='center',color="Black",fontsize=15)
plt.savefig('/home/ubuntu/scripts/graphs/USA.png',dpi=300)
plt.show()


# In[27]:



#setting font scale to increase the legend size as they appeared tiny
print(sns.set(font_scale=1.8))
fig, ax = plt.subplots(1,1,figsize = (20,15))
print(ax.set_aspect('equal'))
print(deaths_merged.plot(column = 'deaths',
                          legend = True , k = 9, alpha=0.8, ax=ax,cmap='YlOrRd',
                       legend_kwds={'label': "\nTotal Deaths",'orientation': "horizontal"}))
print(ctx.add_basemap(ax,zoom=12))
print(plt.title('\nTotal Deaths Excluding Alaska and Hawaii (Last Update: {})'.format(last_update()), fontsize=25))
print(plt.axis('off'))
print(plt.tight_layout())
#creating new columns to store coordinate points to pick up name of each ward to label map
deaths_merged['coords'] = deaths_merged['geometry'].apply(lambda x: x.representative_point().coords[:])
deaths_merged['coords'] = [coords[0] for coords in deaths_merged['coords']]
for idx, row in deaths_merged.iterrows():
    plt.annotate(s=row['STATE_ABBR'], xy=row['coords'],horizontalalignment='center',color="Black",fontsize=15)
plt.savefig('/home/ubuntu/scripts/graphs/USA2.png',dpi=300)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




