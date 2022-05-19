 
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('Risk-based Monitoring System')

st.markdown("""
This app performs simple risk monitoring for clinical trial!
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [Wemedoo.com](https://www.wemedoo.com/)
""")

# load data
query = pd.read_excel(r"QueryManagerExport.xlsx")

# make the columns names to lower case
query.columns = [x.lower() for x in query.columns]

# rename column names
query = query.rename({'query id':'query_id',
                      'description':'query_description', 
                      'trial acronym':'trial', 
                      'organization':'organization',
                      'site id':'site_id',
                      'document name':'document_name',
                      'major version':'major_version',
                      'minor version':'minor_version',
                      'instance id':'instance_id',
                      'patient id':'patient_id',
                      'screening number':'screening_num',
                      'chapter':'chapter',
                      'page':'page',
                      'field':'field',
                      'query status':'query_status',
                      'created by':'created_by',
                      'creation time [utc]':'creation_time',
                      'last update time [utc]':'last_update_time',
                      'last updated by':'last_updated_by',
                      'query type':'query_type'}, axis=1)

query['creation_time'] = query['creation_time'].astype('datetime64[s]')
query['last_update_time'] = query['last_update_time'].astype('datetime64[s]')

# adding event_date column
query['creation_date'] = pd.to_datetime(query['creation_time'].apply(lambda x: x.strftime('%Y-%m-%d')))
query['creation_month'] = pd.to_datetime(query['creation_time'].apply(lambda x: x.strftime('%Y-%m')))

# Sidebar - Site selection
sorted_unique_site = sorted(query.organization.unique())
selected_site = st.sidebar.multiselect('Site', sorted_unique_site, sorted_unique_site)

# Sidebar - Status selection
unique_status = sorted(query.query_status.unique())
selected_status = st.sidebar.multiselect('Status', unique_status, unique_status)

# Filtering data
df_selected_site = query[(query.organization.isin(selected_site)) & (query.query_status.isin(selected_status))]

st.header('Display Query Stats of Selected Site(s)')
st.write('Data Dimension: ' + str(df_selected_site.shape[0]) + ' rows and ' + str(df_selected_site.shape[1]) + ' columns.')
st.dataframe(df_selected_site)
