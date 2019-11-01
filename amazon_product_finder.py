from urllib.parse import urljoin
from selectorlib import Extractor
import requests
from googlesearch import search
import itertools
import json
import time

class scraperAgent():
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev>(KHTML, like Gecko) Chrome/<Chrome Rev> Safari/<WebKit Rev>'
        #user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
        self.headers = { 'User-Agent': self.user_agent }

    def getHtmlContent(self, url):
        return requests.get(url, headers=self.headers)

class googleFinder():
    def __init__(self):
        self.query = ''

    def search(self, query, numResults=5):
        return search(query, tld='com', num=numResults)

class amazonFinder():
    def __init__(self):
        self._baseURL = r"https://www.amazon.com/"
        self._agent = scraperAgent()
        self._productExtractor = Extractor.from_yaml_file('selectors/amazon.yml')
        self._google = googleFinder()

    def extractAmazonProductInfo(self, url):
        html = self._agent.getHtmlContent(url)
        data = self._productExtractor.extract(html.text)
        return data


    def findBestMatch(self, keywords = 'python programming', num_results = 5):
        """
        look through google search results for amazon.
        Find matches
        Make sure keywords are in amazon title
        return productData that has keywords in amazon title.
        """
        results = self._google.search(keywords + ' amazon')

        searchFilters = keywords.split(' ')

        count = 0
        for result in results:

            if ('www.amazon' in result):
                productData = self.extractAmazonProductInfo(result)

                containsFilter = True

                for searchFilter in searchFilters:
                    if (searchFilter  not in productData.get('ProductName')):
                        containsFilter = False

                if (containsFilter):
                    return productData

            if (count > num_results):
                return {}

            count += 1




#google = googleFinder()
#
#result = google.search('cisco SG350-28P-K9 amazon')
#
#print(result)

amazon = amazonFinder()

productData = amazon.findBestMatch(keywords='cisco SG350')

print(productData)




