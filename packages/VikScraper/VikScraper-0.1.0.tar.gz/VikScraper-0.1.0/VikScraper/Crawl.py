import requests
import urllib
from ipywidgets import fixed
from requests_html import HTML
from requests_html import HTMLSession
import time
import urllib3
import re

import itertools
from urllib.parse import  urljoin

import numpy as np
from sklearn.cluster import AffinityPropagation
import distance
from collections import OrderedDict 
import pandas as pd
from requests.adapters import HTTPAdapter, Retry
from duckduckgo_search import DDGS
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import nltk
nltk.download ('wordnet')
nltk.download('omw-1.4')
nltk.download ('stopwords')


np.random.seed(2018)


class Crawl:

    def __init__(self):
        self.title_list = []
        self.link_list = []
        self.search_queries = []
        self.searchTypeDDG = "Search Term"
        self.pdf__list = []
        self.clusterDF = pd.DataFrame()
        self.cluster_list = []
        self.label_list = {}
        self.filePath = ""
    #FUNCTION TO RETRIEVE HTML DATA GIVEN URL (ALSO OBTAINS PDF FILES FOR STORING)
    def get_source(self, url):
        try:
            session = HTMLSession()
            response = session.get(url)
            return response
        except requests.exceptions.RequestException as e:
            print(e)

    #FUNCTION RETURNS THE WEB TITLE OF EACH PDF FILE, USED AS OPPOSED TO THE PDF FILE NAME ITSELF
    #DOES NOT ACCESS INDIVIDUAL URLS, ONLY FINDS TITLES IN THE GOOGLE SEACH QUERIES
    def parse_results(self, response):  
        css_identifier_result = ".tF2Cxc"
        css_identifier_title = "h3"
        css_identifier_link = ".yuRUbf a"
        css_identifier_text = ".VwiC3b"
        results = response.html.find(css_identifier_result)
        output = []
        for result in results:
            output.append(result.find(css_identifier_title, first=True).text)
        return output    
    
    #RETRIEVES PDF FILES FROM DUCKDUCKGO GIVEN QUERY AND QUERY TYPE
    #BACKUP SEARCH - USED WHEN GOOGLE RETURNS 429 TOO MANY QUERIES ERROR
    #RANDOM ERROR MIGHT POP UP WHEN DUCKDUCK GO SEARCH IS RUN, DUE TO IT BEING INCONSISTENT. BEST WAY TO FIX IS TO TERMINATE PROGRAM AND RERUN, OR WAIT FOR GOOGLE SEARCH TO WORK
    def ddgSearch (self, searchTerms, searchType):
        self.title_list = []
        self.link_list = []
        for i in searchTerms:
            term = i + ' filetype:pdf' #add doc/docx, ppt/pptx, xls, xlsx
            if searchType == 'URL':
                term = 'site:' + term
            print (term)
            results = DDGS(term, region='wt-wt', time=None, max_results=100)
            print (results)
            for i in results:
                title = i['title']
                href = i['href']
                self.title_list.append(title)
                print (self.title_list)
                self.link_list.append(href)

    #FUNCTION storeFile OBTAINS PDF FILE, THEN STORES FILE BASED ON USER FILE PATH SPECIFICATION
    #ALSO ADDS PDF NAME TO LIST OF PDFS
    def storeFile (self, url):
        try:
            response = requests.get(url)
            split_URL = url.split("/", -1)[-1]
            self.pdf_list.append(split_URL)
            open(self.filePath + split_URL, "wb").write(response.content)
        except:
            pass

    def removeSpecial (self, pdf_list):
        replace_list = []
        for i in pdf_list:
            replaced = (re.sub('[^a-zA-Z0-9 \n\.]', ' ', i))
            replaced = ''.join(i for i in replaced if not i.isdigit())
            replace_list.append (replaced)
        return replace_list
    
    def createClusters (self):
        pdfs = self.removeSpecial(self.title_list)
        words = np.asarray(pdfs)
        lev_similarity = -1*np.array([[distance.levenshtein(w1,w2) for w1 in words] for w2 in words])
        affprop = AffinityPropagation(affinity="precomputed", damping=0.5)
        affprop.fit(lev_similarity)
        label_list = {}
        key_list = []
        value_list = []
        for cluster_id in np.unique(affprop.labels_):
            exemplar = words[affprop.cluster_centers_indices_[cluster_id]]
            key_list.append(exemplar)
            cluster = np.unique(words[np.nonzero(affprop.labels_==cluster_id)])
            value_list.append(cluster)
            label_list[exemplar] = len(cluster)
            cluster_str = ", ".join(cluster)
        for i in key_list:
            if i in self.cluster_list:
                key_list.remove(i)
            else:
                self.cluster_list.append(i)
        self.clusterDF['Cluster Term'] = key_list
        self.clusterDF['Values'] = value_list
        ranked = dict(sorted(label_list.items(), key=lambda item: item[1]))
        ranked = OrderedDict(reversed(list(ranked.items())))
        ranked = dict(itertools.islice(ranked.items(), 5)) #takes top 5 search terms to then query next
        queries = list(ranked.keys())
        queries = self.removeSpecial(queries)
        print ("Next Queries: ", queries)
        #interact(googleSearch, searchTerms = queries, searchType = 'Search Term')
        self.search_queries = queries
        self.searchTypeDDG = 'Search Term'
        return queries
    
    def googleSearch(self, search_terms):
        #ADD MORE WIDGETS, MAKE IT LOOK CLEANER
        #TEST ON THE TWO OTHER URLS
        for term1 in search_terms:
            print ("Current Query: ", term1)
            term = 'site%3A{}+filetype%3Apdf'.format(urllib.parse.quote_plus(term1))
            searchTm = term1
            link_list = []
            headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
            page=0
            reits = 0
            title_count = []
            while True:
                url = 'https://www.google.com/search?q={}&sxsrf=ACYBGNTx2Ew_5d5HsCvjwDoo5SC4U6JBVg:1574261023484&ei=H1HVXf-fHfiU1fAP65K6uAU&start={}&sa=N&ved=0ahUKEwi_q9qog_nlAhV4ShUIHWuJDlcQ8tMDCF8&biw=1280&bih=561&dpr=1.5'.format(term,page)
                response = self.get_source(url)
                if response.status_code!=200:
                    print (response.status_code)
                    for link in link_list:
                        self.storeFile (link)
                        break
                    time.sleep (1000)
                    continue
                titles = self.parse_results(response)
                for i in titles:
                    self.title_list.append(i)
                    title_count.append(i)
                #get_topic (titleList)
                links = list(response.html.absolute_links)
                google_domains = ('https://www.google.', 
                                'https://google.', 
                                'https://webcache.googleusercontent.', 
                                'http://webcache.googleusercontent.', 
                                'https://policies.google.',
                                'https://support.google.',
                                'https://maps.google.')

                for url in links[:]:
                    if url.startswith(google_domains):
                        links.remove(url)
                page=page+10
                if len(links) < 1:
                    break
                if reits > 5:
                    break
                reits += 1
                for i in links:
                    link_list.append(i)
                pdfNum = len(title_count)
                print ('Number of Files Found For {}: {}'.format(searchTm, pdfNum))
                time.sleep(2)
                #print ('List of URLs found with {}: {}'.format(searchTm, link_list))
            title_count = []
        print ("Storing Files...")
        for link in link_list:
            self.storeFile (link)
    
    def runSearch(self, query_list, queryType, filePathStr):
        self.searchTypeDDG = queryType
        self.search_queries = query_list
        self.filePath = filePathStr
        while True:
            try:
                self.googleSearch (self.search_queries)
                self.search_queries = self.createClusters()
            except:
                #self.ddgSearch(self.search_queries, self.searchTypeDDG)
                print ("Google query limit reached.")
                time.sleep(120)
                continue


crawl = Crawl()
crawl.runSearch(['devry.edu'], 'URL', "Users/vikramnagapudi/Desktop/")