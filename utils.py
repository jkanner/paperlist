import ads
import csv

# -- PARAMLIST is list of headings for internal CSV file (master_paperlist)
PARAMLIST = ['title', 'author1', 'authorList', 'bibcode', 'pubdate', 'year',
                           'journal', 'volume', 'page', 'abstract', 'arxiv', 'dcc', 'tags', 'doi']

# -- FL is field list returned by ADS
FL = ['author', 'first_author', 'bibcode', 'id',
      'year', 'title', 'abstract', 'arxiv_class',
      'jornal','pubdate', 'pub', 'page', 'volume',
      'alternate_bibcode', 'identifier', 'doi']


def get_arxiv(paper):
    for name in paper.identifier:
        if 'arXiv:' in name:
            return name        
    return ''

def get_doi(paper):
    if paper.doi is None:
        return None
    else:
        return paper.doi[0]


def about_gw(paper):
    gw = False

    print('checking: ', paper.title)
    
    abstract = paper.abstract
    title = paper.title[0]

    # -- Default to allowing paper if no abstract is present
    if abstract is None:
        abstract = ''

    if (abstract.find('gravitational') > 0
        or abstract.find('Gravitational') > 0
        or abstract.find('LIGO') > 0):
        gw = True

    print("title:", title)
    if (title.find('gravitational') > 0
        or title.find('Gravitational') > 0
        or title.find('LIGO') > 0):
        gw = True

        
    print('About GW:', gw)
    return gw


def good_bibcode(record):
    bibcode = record.bibcode
    good = True
    code = bibcode[4:8]
    if code == 'AAS.': good = False
    if code == 'HEAD': good = False
    if code == 'APS.': good = False
    if code == 'GCN.': good = False
    return good


def write_ads_record(paperlist, fn='ads_out.csv'):

    print('Writing to file: ', fn)
    with open(fn, 'w') as outfile:
        csvwrite = csv.writer(outfile, quoting=csv.QUOTE_ALL)
        csvwrite.writerow(PARAMLIST)
        
        for p in paperlist:
            print(p.title)            
            dcc = ''
            tags = ''
            arxiv = get_arxiv(p)
            doi = get_doi(p)
            try:
                page = p.page[0]
            except:
                page = None

            
            csvwrite.writerow([p.title[0], p.first_author, p.author, p.bibcode, p.pubdate, p.year, p.pub, p.volume, page, p.abstract, arxiv, dcc, tags, doi])

    return 0
