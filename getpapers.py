
import ads
import csv

from utils import write_ads_record, FL

#bib = '2021arXiv210707129M'
#fn = 'single.csv'

#papers = list(ads.SearchQuery(bibcode=bib, fl=FL))
#papers = list(ads.SearchQuery(author='Weinstein,Alan', year=2023, fl=FL))
#print(papers)
#write_ads_record(papers, fn)
#print("Wrote result to: ", fn)


def getpapers(author='Kanner,Jonah', year=2023, fl=FL):
    papers = list(ads.SearchQuery(author=author, year=year, fl=FL))
    fn = 'out/paperlist-' + author.replace(",", '-') + str(year) + '.csv'
    write_ads_record(papers, fn)
    return(fn)