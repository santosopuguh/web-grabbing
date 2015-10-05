from lxml import etree
import urllib2 as ul2
import socket as sc
import re
import json
from urlparse import urlparse

class WebCrawl():

    def __init__(self, url):
        self.url = url
        self.domain = ''
        self.ip = ''
        self.tree = ''
        self.title = ''
        self.html_page = ''

    def getDomain(self):
        parsed_url= urlparse(self.url)
        #self.domain = '{url.scheme}://{url.netloc}/'.format(url=parsed_url)
        self.domain = '{url.netloc}'.format(url=parsed_url)
        print 'Domain Name:', self.domain

    def getIP(self):
        self.ip = sc.gethostbyname_ex(self.domain)
        print 'IP Address:', self.ip

    def getContent(self):
        #self.content = lx.parse(self.url)
        web_url = ul2.urlopen(self.url)
        info = web_url.info()
        response = web_url.getcode() #get url respond code (200, etc...)
        print '\nDetail Information:\n', info

        if response == 200:
            self.html_page = web_url.read() #get page source
            #print html_page
            self.tree = etree.HTML(self.html_page)
        else:
            print 'Something\'s wrong'

    def getTitle(self):
        self.title = self.tree.xpath('//title/text()')
        if self.title:
            print 'Page Title:', self.title
        else:
            print 'No Page Title'
    
    def getJSON(self):
        try:
            the_json = json.loads(self.html_page)
            if the_json:
                if 'title' in the_json['metadata']:
                    print 'Title:', the_json['metadata']['title']
                for i in the_json['features']:
                    print '\nPlace:', i['properties']['place'], '\nMagnitude:', i['properties']['mag'], '\nCoordinates:', i['geometry']['coordinates']
        except:
            print 'No JSON'
                        

    def getData(self):
        self.getDomain()
        self.getIP()
        self.getContent()
        self.getTitle()
        self.getJSON()

if __name__ == '__main__':
    url = raw_input('Enter URL: ')
    url_ip = re.findall(re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'), url)
    url_plainText = re.findall(re.compile(r'(\w)'), url)
    print url_ip
    if url_ip:
        print 'It\'s IP Address, Not URL'
      
    else:
        #http://on.doi.gov/1KlE5IQ
        objCrawl = WebCrawl(url)
        objCrawl.getData()
