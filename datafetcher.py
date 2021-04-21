# -*- coding: utf-8 -*-
"""DataFetcher

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tog_D-ULCUhLJb5vUg5TKow0NdTa97r2

A modified version of Chris's code to fetch data

This will get the most current NMOCD data on wells and Facilities
"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install fiona
# !pip install geopandas

"""Import packages and libraries
(imported more than necessary)
"""

from ftplib import FTP
import requests
import time
import fiona
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import animation, rc
import datetime
import seaborn as sns
from sklearn.cluster import DBSCAN
from geopy.distance import great_circle
from shapely.geometry import MultiPoint

##################################
## DOWNLOAD AND CLEAN WELL DATA ##
##################################

"""
Unzip the geodatabase (gdb) and read it using geopandas (gpd). I'm getting the data from the Github repo,
but you could also manually upload the files if you want new data.
I then clean some columns and change the column names for clarity later on.
"""

#Unzip the geodatabase -  take out comments to download from the nmocd site
#!wget https://raw.githubusercontent.com/christopher-reed/UCLA-New-Mexico/master/data/geospatial/NMOCD_GISData.gdb.zip
#!unzip /content/NMOCD_GISData.gdb.zip

# Parse feature class from gdb
df_wells = gpd.read_file('/content/NMOCD_GISData.gdb')

# Clean spud dates
df_wells['spud_date'] = pd.to_datetime(df_wells['spud_date'], errors = 'coerce')
df_wells['year_spudded'] = df_wells['spud_date'].dt.year
df_wells['effective_date'] = pd.to_datetime(df_wells['effective_date'], errors = 'coerce')
df_wells['plug_date'] = pd.to_datetime(df_wells['plug_date'], errors = 'coerce')

# change this area of coding to the county wanted
df_Well_by_county = df_wells[(df_wells['county'] == 'Lea') &
                        (df_wells['status'] == 'Active')]

# New column names
# Can use list comprehension bc no edge cases
#new_well_column_names = ['well_' + x for x in df_wells.columns]
#df_wells.columns = new_well_column_names

######################################
## DOWNLOAD AND CLEAN FACILITY DATA ##
######################################

df_facilities = pd.read_csv('https://raw.githubusercontent.com/christopher-reed/UCLA-New-Mexico/master/data/geospatial/nm_facilities.csv')

# Function to handle edge cases where col name already has facility
def rename_fac_cols(x):

  x = x.lower().replace(' ', '_')

  if 'facility' not in x:
    return 'facility_' + x
  else:
    return x

new_facility_column_names = [rename_fac_cols(x) for x in df_facilities.columns]
df_facilities.columns = new_facility_column_names 

df_facilities_by_county = df_facilities[(df_facilities['facility_county'] == 'Lea')]

# #Save raw data
df_Well_by_county.to_csv('Lea_wells.csv')
df_facilities_by_county.to_csv('Lea_Facilities.csv')



