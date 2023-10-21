#!/usr/bin/env python
# coding: utf-8

# ### PART4: Share your ideas or functions to address below errors
# •	Error1: reversed dates 
# Reversed dates: if end_date is earlier than start_date. e.g. 
# 
# 
# ![image.png](attachment:image.png)

# **Idea** - Reverse start and end dates for any rows where start_date > end_date

# In[1]:


from IPython.display import display

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(color_codes=True)

import warnings
warnings.filterwarnings('ignore')

import missingno as mnso


# In[2]:


"""
UDF: fix_date() accepts the data frame as an input and reverses them if start date>end date
"""

def fix_date(df):
    #-------------------Convert start and end date to date time format in Pandas
    #-----If there are any parsing errors during the conversion, the problematic values will be set to NaT
    
    df['start_date'] = pd.to_datetime(df['start_date'], format='%d-%m-%Y', errors='coerce')
    
    df['end_date'] = pd.to_datetime(df['end_date'], format='%d-%m-%Y', errors='coerce')

    # Extracting rows with reverse dates
    reversed_dts = df[df['end_date'] < df['start_date']]

    #----Checking if rows with reverse date exists: If yes, display them and swap
    #----Print function can be hidden for larger datasets
    if not reversed_dts.empty:
        
#         print("Reversed Dates:")
#         print(reversed_dts)
        #---Swapping the start_date and end_date for rows with reversed dates
        df.loc[df['end_date'] < df['start_date'], ['start_date', 'end_date']]         = df.loc[df['end_date'] < df['start_date'], ['end_date', 'start_date']]

    return df


# In[3]:


#--------Creating a Sample Data
data = {
    'Supplier': ['C', 'C'],
    'Supplier_Product': [2496186, 2498095],
    'Ref_No': [-2607899, -2607904],
    'start_date': ['21-03-2021', '21-03-2021'],
    'end_date': ['20-03-2021', '20-03-2021'],
    'QtyFct': [1, 1]
}

df = pd.DataFrame(data)

display(df)

# Check and fix reversed dates
df = fix_date(df)

print("-------------After Fixing-----------------")

# Display the updated DataFrame
display(df)


# ### •	Error2: Overlapping days
# Overlapping days: for same ‘Supplier_Product’ if there are any overlapping days between previous end_date and current start_date. e.g.
# 
# ![image.png](attachment:image.png)

# **Idea 1**: We delete any overlap rows here. The idea is to keep the first instance of the row and then remove the rest.
# 
# 
# **Idea 2**: We replace the end date with max end date of all overlaping instances. This function won't handle if there are multiple suppliers. We need to retweak it to handle different suppliers with overlaping instances.

# In[4]:


"""
We delete any overlap rows here. The idea is to keep the first instance of the row and then remove the rest.
"""
def delete_overlap_instances_except_first(df, index):
    
    return  df.drop(index=index) #----drop all indexes identified as overlapping except first occurance


# In[5]:


"""
We replace the end date with max end date of all overlaping instances. This function won't handle if there are
multiple suppliers. We need to retweak it to handle different suppliers with overlaping instances.
"""

def replace_end_dt_of_first_instance_with_largest_end_date(df, index):
    
#     print(index)
    
    df_rows_overlap= df.iloc[index] #---Identify overlapping index
    
    max_date = df_rows_overlap['end_date'].max() #----Indentify max date
    
    df=df.drop(index=index) #---drop overlap instances
    
    df.at[index[0]-1,'end_date']=max_date #----assing end date of first occurance to max date
    
    return df


# In[6]:


import pandas as pd

def check_and_fix_overlapping_days(df):
    
    #---------#-------------------Convert start and end date to date time format in Pandas
    #-----If there are any parsing errors during the conversion, the problematic values will be set to NaT
    
    df['start_date'] = pd.to_datetime(df['start_date'], format='%d-%m-%Y', errors='coerce')
    df['end_date'] = pd.to_datetime(df['end_date'], format='%d-%m-%Y', errors='coerce')
    
    df['Supplier_Product_Key']=df['Supplier']+"-"+(df['Supplier_Product'].astype(str))

    #-------------Order the data by Supplier Product Key
    df = df.sort_values(by=['Supplier_Product_Key', 'start_date'])

    # ------ Declaring variable to store previous date
    prev_end_date = None
    prev_supplier_product=None

    #---------List to store indexes of rows with overlapping days
    overlapping_indices = []

    for index, row in df.iterrows():
        
        if prev_end_date is not None and prev_supplier_product is not None and row['Supplier_Product_Key']==prev_supplier_product and row['start_date'] <= prev_end_date:
            overlapping_indices.append(index)

        else:
            prev_end_date = row['end_date']
            prev_supplier_product = row['Supplier_Product_Key']

    if overlapping_indices:
        print("Overlapping Days Found:")
        print(overlapping_indices)
        
    print("Solution 1: We delete any overlap rows here. The idea is to keep the first instance of the row and then remove the rest")

    display(delete_overlap_instances_except_first(df,overlapping_indices))
    
    
    print("Solution 2: We replace the end date  of first occurance with max end date of all overlaping instances and drop rest")
    display(replace_end_dt_of_first_instance_with_largest_end_date(df,overlapping_indices))
    


# In[7]:


# Sample data
data = {
    'Supplier': ['C', 'C', 'C', 'C'],
    'Supplier_Product': [2496185, 2496186, 2496186, 2496186],
    'Ref_No': [-2607811, -2607899, -2607904, -2607904],
    'start_date': ['20-03-2013', '10-01-2014', '01-02-2018', '01-05-2018'],
    'end_date': ['21-03-2013', '31-12-2019', '08-02-2020', '08-05-2020'],
    'QtyFct': [1, 1, 1, 1]
}

df = pd.DataFrame(data)

display(df)

# Check and handle overlapping days
df = check_and_fix_overlapping_days(df)

# Display the updated DataFrame
display(df)

