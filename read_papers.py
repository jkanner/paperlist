import csv
import ads
from io import StringIO


# ----------
# Define article record class
# ----------
def get_authstr(article):
    author = eval(article['authorList'])  # -- Convert string to list
    auth_str = ''
    auth_count = 0
    for auth in author:
        if auth_count > 5:
            auth_str += 'et. al., '
            break
        try:
            spl = auth.split(',')
            auth_str += spl[1] + ' ' + spl[0] + ', '
        except:
            auth_str += auth + ', '
        auth_count += 1        
    return auth_str

class ArticleList:

    def __init__(self, filename):        
        #reader = csv.reader(open(filename, 'r', encoding='utf-8'))
        reader = csv.reader(StringIO(filename.getvalue().decode("utf-8")))
        need_names = True
        self.alist = []
        for row in reader:

            if need_names:
                self.nameList = row
                need_names = False
            else:
                data = {}
                for name, value in zip(self.nameList, row):
                    #data[name] = value
                    data[name] = value
                self.alist.append(data)

    def writehtml(self, filename, start=2007, stop=2016):
        outfile = open(filename, 'w')
        outfile.write('<html><head><meta charset="UTF-8"><title>Publications</title></head><body>\n\n')
        outfile.write("""
<style>
li {
    margin: 0 0 10px 0;
   } 
</style>

""")
        for thisyear in range(stop, start-1, -1):
            outfile.write('<h3>{0}</h3> \n\n'.format(thisyear))
            for article in sorted(self.alist, key=lambda x: x['title']):
                
                title = article['title']
                print("Writing ...", title)
                dcc = article['dcc']
                bibcode = article['bibcode']
                yr = int(article['year'])
                if int(yr) != int(thisyear): continue
                journal = '<i>' + article['journal'] + '</i>' + ' ' + '<b>' + article['volume'] + '</b>' + ' ' + article['page']
                
                arxiv = article['arxiv']
                auth_str = get_authstr(article)
                bib_str = '<b>' + title + '</b>. '  + auth_str + journal + " (" + str(yr) + ") "
                
                try:
                    outfile.write(str(bib_str))
                except:
                    outfile.write(bib_str)
                if len(bibcode)>1:
                    outfile.write(" <a href='http://adsabs.harvard.edu/abs/{0}'>ADS</a>".format(bibcode))
                if len(arxiv)>1:
                    arxiv_url = 'https://arxiv.org/abs/{0}'.format(arxiv.split(':')[1])
                    outfile.write(" <a href='{0}'>{1}</a>".format(arxiv_url, arxiv))
                if len(dcc)>1:
                    outfile.write(" <a href='https://dcc.ligo.org/{0}'>DCC</a> ".format(dcc))
                if len(article['doi'])>1:
                    outfile.write(" <a href='https://doi.org/{0}'>DOI:{0}</a> ".format(article['doi']))
                    
                outfile.write('  <br/><br/><br/>\n')
        outfile.write('</body></html>')    
        outfile.close()

    def writebibitem(self, filename, start=2007, stop=2016):
        outfile = open(filename, 'w')
        outfile.write("""
        \\documentclass{article}
        \\begin{document}
        \\begin{thebibliography}{99}
        """)

        for art in sorted(self.alist, key=lambda x: x['title']):
            bib_str = ''
            bib_str += '\\bibitem{'
            bib_str += art['bibcode']
            bib_str += '}'
            bib_str += " \\emph{" + art['title'] + "} "
            bib_str += get_authstr(art)
            bib_str += " " + art['journal']
            bib_str += "(" + art['pubdate'] + ")"
            #bib_str += art['journal'].split(',')[0]
            #try:
            #    bib_str += " \\textbf{" + art['volume'] + "} " + art['page']
            #except:
            #    pass
            outfile.write("\n" + bib_str + "\n")

        outfile.write("""
        \\end{thebibliography}
        \\end{document}
        """)
        outfile.close()

    def writetext(self, filename, start=2007, stop=2016):
        outfile = open(filename, 'w')
        #for article in sorted(self.alist, key=lambda x: x['title']):
        for article in self.alist:
            title = article['title']
            bibcode = article['bibcode']
            yr = article['year']
            journal = article['journal']
            auth_str = get_authstr(article)
            bib_str = ' "' + title + '" '  + auth_str + journal + " (" + str(yr) + ") "
            try:
                outfile.write(bib_str.encode('utf-8') + '\n\n')
            except:
                outfile.write(bib_str + '\n\n')
        outfile.close()


    def write_bibtex(self, filename):

        # -- Get list of bibcodes
        biblist = []
        for article in self.alist:
            biblist.append(article['bibcode'])
        outfile = open(filename, 'w')
        bibtex = ads.ExportQuery(bibcodes=biblist, format='bibtex').execute()
        outfile.write(bibtex)
        outfile.close()
        
                      
# def main():
    
if __name__ == "__main__":    
    
    #filename = 'paperlist_2021'
    
    #filename = 'update_2021'
    #filename = 'merged_list'
    filename = 'master_paperlist'
    #filename  = 'new_papers' 
    
    al = ArticleList(filename+'.csv')
    for article in al.alist:
        for key in article.keys():
            print(key, article[key])

    al.writehtml(filename+'.html', start=2006, stop=2021)
    al.writebibitem(filename+'.tex', start=2016, stop=2021)
    al.writetext(filename+'.txt', start=2016, stop=2021)
    al.write_bibtex(filename+'.bib')
    
    


