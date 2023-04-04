import streamlit as st
from getpapers import getpapers
import time, io, csv

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
    
    outfile = st.session_state['csv']
    results = outfile.getvalue().split('\n')
    st.write("Found {0} results".format(len(results)-2))
    btn = st.download_button('Download', data=outfile.getvalue(), file_name=fn)

    


    



