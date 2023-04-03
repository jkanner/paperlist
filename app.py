import streamlit as st
from getpapers import getpapers

st.write("# Group Paper List")


with st.form("queryform"):
    
    authorf = st.text_input('Author First Name')

    authorl = st.text_input('Author Last Name')

    year = st.number_input('Year', min_value=2000, max_value=2040, value=2023)

    author = authorl + ',' + authorf
    fn = 'out/paperlist-' + author.replace(",", '-') + str(year) + '.csv'
    try:
        token=st.secrets['token']
    except:
        token=None
        
    submitted = st.form_submit_button("Query",
                                      on_click=getpapers,
                                      args=(author, year, token)
                                      )


if submitted:
    with open(fn, 'r') as file:
        btn = st.download_button('Download', data=file, file_name='papers.csv')
    


    



