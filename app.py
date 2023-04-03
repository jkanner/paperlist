import streamlit as st
from getpapers import getpapers
import time

st.write("# Group Paper List")


st.write("## Instructions")

st.write("""

1. Check out the [LIGO Lab Group paper list](https://docs.google.com/spreadsheets/d/1zxE7Zlatfgl07ocoJe-1LpNOeFOKHjFjLxplOxGlKzI/edit?usp=sharing)

2. Use the form below to query for your recent papers

3. Download the CSV, and then copy and paste the data into the paper list

""")


with st.form("queryform"):
    
    authorf = st.text_input('Author First Name')

    authorl = st.text_input('Author Last Name')

    year = st.number_input('Year', min_value=2000, max_value=2040, value=2023)

    author = authorl + ',' + authorf
    fn = 'paperlist-' + author.replace(",", '-') + str(year) + '.csv'
    try:
        token=st.secrets['token']
    except:
        token=None
        
    submitted = st.form_submit_button("Query",
                                      on_click=getpapers,
                                      args=(author, year, token)
                                      )


if submitted:
    try:
        with open(fn, 'r') as file:
            btn = st.download_button('Download', data=file, file_name='papers.csv')
    except:
        st.write("Whoops!  Try clicking the query button again.")
    


    



