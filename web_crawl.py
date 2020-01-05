''' web crawl. '''
import re
import json
from json.decoder import JSONDecodeError
import socket as sc
import urllib.request as ul2
from urllib.parse import urlparse
from lxml import etree


class WebCrawl():
    ''' Web crawl. '''

    def __init__(self, url):
        self.url = url
        self.domain = ''
        self.ip_address = ''
        self.tree = ''
        self.title = ''
        self.html_page = ''

    def get_domain(self):
        ''' Get domain. '''
        parsed_url = urlparse(self.url)
        #self.domain = '{url.scheme}://{url.netloc}/'.format(url=parsed_url)
        self.domain = '{url.netloc}'.format(url=parsed_url)
        print('Domain Name:', self.domain)

    def get_ip(self):
        ''' Get ip address. '''
        self.ip_address = sc.gethostbyname_ex(self.domain)
        print('IP Address:', self.ip_address)

    def get_content(self):
        ''' Get content. '''
        #self.content = lx.parse(self.url)
        web_url = ul2.urlopen(self.url)
        info = web_url.info()
        response = web_url.getcode() #get url respond code (200, etc...)
        print('\nDetail Information:\n', info)

        if response == 200:
            self.html_page = web_url.read() #get page source
            self.tree = etree.HTML(self.html_page)
        else:
            print('Something\'s wrong')

    def get_title(self):
        ''' Get page tite. '''
        self.title = self.tree.xpath('//title/text()')
        if self.title:
            print('Page Title:', self.title)
        else:
            print('No Page Title')

    def get_json(self):
        ''' Get JSON if any. '''
        try:
            the_json = json.loads(self.html_page)
            if the_json:
                if 'title' in the_json['metadata']:
                    print('Title:', the_json['metadata']['title'])
                for i in the_json['features']:
                    print('\nPlace:', i['properties']['place'], '\nMagnitude:', \
                        i['properties']['mag'], '\nCoordinates:', i['geometry']['coordinates'])
        except JSONDecodeError as error:
            print('JSONDecoderError: \n', error)

    def get_data(self):
        ''' Get data from method. '''
        self.get_domain()
        self.get_ip()
        self.get_content()
        self.get_title()
        self.get_json()

if __name__ == '__main__':
    URL = input('Enter URL: ')
    URL_IP = re.findall(re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'), URL)
    # url_plainText = re.findall(re.compile(r'(\w)'), URL)
    print(URL_IP)
    if URL_IP:
        print('It\'s IP Address, Not URL')
    else:
        # http://on.doi.gov/1KlE5IQ
        WEB_CRAWL = WebCrawl(URL)
        WEB_CRAWL.get_data()
