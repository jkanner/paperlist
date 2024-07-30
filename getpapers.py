
import ads
import csv
import streamlit as st
from utils import write_ads_record, FL, about_gw, good_bibcode, is_shortauthor
import time

#bib = '2021arXiv210707129M'
#fn = 'single.csv'

#papers = list(ads.SearchQuery(bibcode=bib, fl=FL))
#papers = list(ads.SearchQuery(author='Weinstein,Alan', year=2023, fl=FL))
#print(papers)
#write_ads_record(papers, fn)
#print("Wrote result to: ", fn)


def getpapers(token=None, fl=FL ):

    author = st.session_state['authorl'] + ',' + st.session_state['authorf']
    year = st.session_state['year']
    year = str(year)

    try:
        papers = list(ads.SearchQuery(author=author, year=year, fl=FL, token=token))     
    except:
        st.write('Whoops!  Please retry query')
        return(0)
    fn = 'paperlist-' + author.replace(",", '-') + str(year) + '.csv'

    # -- Filter out conference talks
    papers = [x for x in papers if good_bibcode(x)]

    # -- filter out full author list papers
    if st.session_state['shortauthor']:
        papers = [x for x in papers if is_shortauthor(x)]
        
    # -- Try filtering on gw content
    gw_papers = [x for x in papers if about_gw(x)]

    print('Paper list', papers)
    # -- Return paper list
    if st.session_state['gwfilter']:
        write_ads_record(gw_papers)
    else:
        write_ads_record(papers)

    return(fn)
