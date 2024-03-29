from urllib.parse import urljoin
from selectorlib import Extractor
from scraper_agent import scraperAgent
from google_finder import googleFinder
from amazon_item import amazonItem
import itertools
import json
import time

class amazonFinder():
    def __init__(self):
        self._baseURL = r"https://www.amazon.com/"
        self._agent = scraperAgent()
        self._productExtractor = Extractor.from_yaml_file('selectors/amazon.yml')
        self._google = googleFinder()

    def extractAmazonProductInfo(self, url):
        html = self._agent.getHtmlContent(url)
        data = self._productExtractor.extract(html.text)
        dataEmpty = self._checkThatDataIsNotEmpty(data)
        if (dataEmpty): # try again with a different user agent. I only do this once so I don't spin indefinitely
            self._agent.switchUserAgent()
            html = self._agent.getHtmlContent(url)
            data = self._productExtractor.extract(html.text)

        return data

    def _checkThatDataIsNotEmpty(self, data):
        """
        look through the extracted data and validate that the data fields are populated. If not likely we're blocked by a captcha
        """
        for key in data.keys():
            if data.get(key) != []:
                return False

        return True


    def findBestMatch(self, keywords = 'python programming', num_results = 5):
        """
        look through google search results for amazon.
        Find matches
        Make sure keywords are in amazon title
        return productData that has keywords in amazon title.
        """
        print("searching for %s..."%keywords)

        results = self._google.search(keywords + ' amazon')

        searchFilters = keywords.split(' ')

        count = 0
        for result in results:

            if ('www.amazon' in result):
                productData = self.extractAmazonProductInfo(result) #todo: use amazonItem to filter data.

                containsFilter = False

                titleLower = productData.get('ProductName')
                if titleLower != None and titleLower != []:

                    containsFilter = True
                    titleLower = titleLower.lower()
                    for searchFilter in searchFilters:
                        sf = searchFilter.lower()

                        if (sf  not in titleLower):
                            containsFilter = False

                if (containsFilter):
                    item = amazonItem(productData)

                    item.parseData(result)

                    return item

            if (count > num_results):
                return None

            count += 1
            # incase we're going through a bunch of amazon listings sleep so we don't hammer amazon.
            time.sleep(2) 




#google = googleFinder()
#
#result = google.search('cisco SG350-28P-K9 amazon')
#
#print(result)

if __name__ == "__main__":
    amazon = amazonFinder()

    productData = amazon.findBestMatch(keywords='cisco SG350')

    productData.printItem()
