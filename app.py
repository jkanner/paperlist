import streamlit as st
from getpapers import getpapers
import time, io, csv
from read_papers import ArticleList


st.write("# Group Paper List")


st.write("## Instructions")

st.write("""

1. Check out the LIGO Lab Group [master paper list](https://docs.google.com/spreadsheets/d/1zxE7Zlatfgl07ocoJe-1LpNOeFOKHjFjLxplOxGlKzI/edit?usp=sharing)

2. Use the form below to query for your recent papers

3. Click "Download CSV"

4. Copy and paste any new papers into the master paper list

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
        with open('/Users/jkanner/.ads/dev_key', 'r') as infile:
            token=infile.read()
    
    submitted = st.form_submit_button("Query",
                                      on_click=getpapers,
                                      args=(author, year, token)
                                      )


if submitted:
    
    outfile = st.session_state['csv']
    results = outfile.getvalue().split('\n')
    numresults = len(results)-2
    st.write("Found {0} results".format(len(results)-2))
    if numresults == 50:
        st.write("⚠️ **Warning:**  _You may need to press the Query button again_")
    btn = st.download_button('Download CSV', data=outfile.getvalue(), file_name=fn)

    

st.write('---')
st.write('## File Format Converter')
st.write('### Instructions')
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


    



