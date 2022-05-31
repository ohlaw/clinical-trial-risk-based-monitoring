 
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
#import plost
import plotly.express as px
import datetime


# load data
def load_data():
    df = pd.read_excel(r"QueryManagerExport.xlsx") 
    df.columns = [x.lower() for x in df.columns]  # make the columns names to lower case

    # rename column names
    df = df.rename({'query id':'query_id',
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
    
    df['creation_time'] = df['creation_time'].astype('datetime64[s]')
    df['last_update_time'] = df['last_update_time'].astype('datetime64[s]')
    
    # adding event_date column
    df['creation_date'] = pd.to_datetime(df['creation_time'].apply(lambda x: x.strftime('%Y-%m-%d')))
    df['creation_month'] = pd.to_datetime(df['creation_time'].apply(lambda x: x.strftime('%Y-%m')))

    return df


# Sidebar - Date selection
def df_filter(message, df):

    slider_1, slider_2 = st.sidebar.date_input('%s' % (message), [df['creation_date'].min(), df['creation_date'].max()])

    st.info('Start: **%s** End: **%s**' % (slider_1, slider_2))

    start_date = datetime.datetime.strptime(str(slider_1), '%Y-%m-%d')
    end_date = (datetime.datetime.strptime(str(slider_2), '%Y-%m-%d'))

    delta = end_date - start_date   # returns timedelta
    
        
    selected_date = [start_date + datetime.timedelta(days=i) for i in range(delta.days + 1)]

    # Sidebar - Site selection
    sorted_unique_site = sorted(df.organization.unique())
    selected_site = st.sidebar.multiselect('Site', sorted_unique_site, sorted_unique_site)

    # Sidebar - Status selection
    unique_status = sorted(df.query_status.unique())
    selected_status = st.sidebar.multiselect('Status', unique_status, unique_status)

    # Filtering data
    filtered_df = df[(df.creation_date.isin(selected_date)) & (df.organization.isin(selected_site)) & (df.query_status.isin(selected_status))]

    return filtered_df


if __name__ == '__main__':

    # Page setting
    st.set_page_config(layout="wide")

    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.title('Risk-based Monitoring System')

    st.markdown("""
    This app performs simple risk monitoring for clinical trial!
    * **Python libraries:** base64, pandas, streamlit
    * **Data source:** [Wemedoo.com](https://www.wemedoo.com/)
    """)

    df = load_data()
    selected_df = df_filter('Move slider to filter dataframe', df)
    
    st.header('Display Query Stats of Selected Site(s)')

        # Create three columns
    col1,col2,col3 = st.beta_columns(3)

    with col1:
        st.header("A cat")

    with col2:
        st.header("A dog")

    with col3:
        st.header("An owl")

        
    st.write('Data Dimension: ' + str(selected_df.shape[0]) + ' rows and ' + str(selected_df.shape[1]) + ' columns.')
    st.dataframe(selected_df)

    selected_df.to_csv('output.csv', index=False)
    df = pd.read_csv('output.csv')












# Number of query per site
if st.button('Number of query per site'):
    st.header('Sites And Their Frequency of Query')
    

    query_per_site = df.groupby('organization')['query_id'].nunique().sort_values(ascending=False).reset_index()

    fig, ax = plt.subplots(figsize=(18,8))
    ax = sns.barplot(data=query_per_site, x='query_id', y='organization')
    plt.title('Sites And Their Frequency Of Query', size=20)
    plt.ylabel('Organization', size=13)
    plt.xlabel('Number of Query', size=13)
    st.pyplot(fig)

# Top 10 Organization By Number of Query
if st.button('Top 10 Sites'):
    st.header('Top 10 Organization By Number of Query')

    top_organization = df['organization'].head(10)

    # create dataframe for the top 10 platforms
    top_org = df[df['organization'].isin(top_organization)]

    # Calculate the proportions of the shares of the chains of each of the establishment
    top_org['proportion'] = ((top_org['query_id'] * 100) / 
                                   df['query_id'].sum()).round(1)

    top_org = top_org.sort_values(by='proportion', ascending=False)

    fig, ax = plt.subplots(figsize=(10, 7))
    ax = sns.barplot(x="organization", y="proportion", data=top_org)
    plt.title('Top 10 Organization by Number of Query', size=15)
    plt.xlabel("Name of Organization", size=13)
    plt.xticks(rotation=70)
    plt.ylabel('Proportion (100%)', size=13)
    st.pyplot(fig)



