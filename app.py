import streamlit as st
from getpapers import getpapers
import time, io, csv
from read_papers import ArticleList


st.write("# LIGO Laboratory Paper List")

st.write("""
    The lab would like your help keeping track of papers published by LIGO Lab personnel.  
    Please use the tools below to add your recent papers to the lab paper list.

    For help, please contact Jonah Kanner.
    """)  

st.write("## To Add Papers:")

st.write("""

1. Use the form below to query [ADS](https://ui.adsabs.harvard.edu) for your recent papers.  You may need to click "Query" twice.

2. Click "Download CSV" to download a CSV file of your papers.

3. Copy and paste any new papers into the [master paper list](https://docs.google.com/spreadsheets/d/1SOAwgqzmDrWgAXbfwao-nQvLYZgeKXiw5yterqiG9eM/)

4. Add the DCC number of each paper to the appropriate column.

5. Add TRUE as needed to the last 3 columns to indicate if each paper is about data analysis, instrument science, and/or if it is a full author-list LVK paper.
""")

with st.form("queryform"):
    
    authorf = st.text_input('Author First Name', key='authorf')

    authorl = st.text_input('Author Last Name', key='authorl')

    year = st.number_input('Year', min_value=2000, max_value=2040, value=2023, key='year')

    gwfilter = st.checkbox('Return only papers about gravitational-waves?', value=True, key='gwfilter')

    shortauth = st.checkbox('Return only short author-list papers?', value=True, key='shortauthor')

    author = authorl + ',' + authorf
    fn = 'paperlist-' + author.replace(",", '-') + str(year) + '.csv'
    try:
        token=st.secrets['token']
    except:
        with open('/Users/jkanner/.ads/dev_key', 'r') as infile:
            token=infile.read()
    
    submitted = st.form_submit_button("Query ADS",
                                      on_click=getpapers,
                                      args=(author, year, token, gwfilter, shortauth)
                                      )


if submitted:
    
    outfile = st.session_state['csv']
    results = outfile.getvalue().split('\n')
    numresults = len(results)-2
    st.write("**Found {0} results:**".format(len(results)-2))
    if numresults == 50:
        st.write("⚠️ **Warning:**  _You may need to press the Query button again_")

    for paper in st.session_state['papers']:
        st.write("> " + paper.title[0])
    btn = st.download_button('Download CSV', data=outfile.getvalue(), file_name=fn)

    

st.write('---')
st.write('## File Format Converter')
st.write('#### To download HTML, LATEX, BIBTEX, or ASCII:')
st.write('1. Upload a paper list CSV file')
st.write('2. You can then download the paper list in different formats')

infile = st.file_uploader('Upload CSV Paper List', type='csv', help='The file should be a paper list in CSV format')


if infile:
    al = ArticleList(infile)
    al.writehtml('upload.html', start=2000, stop=2024)
    al.writetext('upload.txt', start=2000, stop=2024)
    al.write_bibtex('upload.bib', token=token)
    al.writebibitem('upload.tex', start=2000, stop=2024)

    

    with open('upload.html','r') as outfile:
        btn = st.download_button(
            label='Download HTML',
            data=outfile,
            file_name='papers.html',
            mime="text/html")

    with open('upload.txt','r') as outfile:
        btn = st.download_button(
            label='Download TXT',
            data=outfile,
            file_name='papers.txt',
            mime="text/plain")

    with open('upload.bib','r') as outfile:
        btn = st.download_button(
            label='Download BIBTEX',
            data=outfile,
            file_name='papers.bib',
            mime="text/plain")

    with open('upload.tex','r') as outfile:
        btn = st.download_button(
            label='Download LATEX',
            data=outfile,
            file_name='papers.tex',
            mime="text/plain")


    



