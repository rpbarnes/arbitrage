from urllib.parse import urljoin
from selectorlib import Extractor
from googlesearch import search
from scraper_agent import scraperAgent
import itertools
import json
import inspect
import time


class googleFinder():
    def __init__(self):
        self.query = ''

    def search(self, query, numResults=5):
        return search(query, tld='com', num=numResults)


class amazonItem():
    def __init__(self, response):
        self.__response = response
        self.__initializeClass()
    
    def parseData(self, url):
        self.__getPrice()
        self.__productName = self.__response.get("ProductName")
        self.__productType = self.__response.get("ProductType")
        self.__productCategory = self.__response.get("ProductCategory")
        self.__availability = self.__response.get("Availability")
        self.__categoryRank = self.__response.get("CategoryRank")
        self.__parseProductInformation()
        self.__itemURL = url

        self.__fillDict()

    def __initializeClass(self):
        self.__itemURL = None
        self.__productName = None
        self.__productType = None
        self.__productCategory = None
        self.__availability = None
        self.__categoryRank = None
        self.__bestSellersRank = None
        self.__asin = None
        self.__price = None
        self.__model = None
        self.__shippingWeight = None
        self.__itemWeight = None
        self.__dateFirstListed = None

    @property
    def itemURL(self):
        return self.__itemURL

    @property
    def itemWeight(self):
        return self.__itemWeight

    @property
    def productName(self):
        return self.__productName

    @property
    def productType(self):
        return self.__productType

    @property
    def productCategory(self):
        return self.__productCategory

    @property
    def availability(self):
        return self.__availability

    @property
    def categoryRank(self):
        return self.__categoryRank

    @property
    def bestSellersRank(self):
        return self.__bestSellersRank

    @property
    def asin(self):
        return self.__asin

    @property
    def price(self):
        return self.__price

    @property
    def shippingWeight(self):
        return self.__shippingWeight

    @property
    def model(self):
        return self.__model

    @property
    def dateFirstListed(self):
        return self.__dateFirstListed

    def __parseProductInformation(self):
        """
        Parse product string information.

        Given a list of search terms. Look for those terms in the product information string. find the position of those terms. then go through the product information string, given position of indecies, and pull out necessary product information.
        """
        searchTerms = [
            [ 'Product Dimensions', -1 ],
            [ 'Item Weight', -1 ], 
            [ 'Shipping Weight', -1 ],
            [ 'ASIN', -1 ],
            [ 'Item model number', -1 ],
            [ 'Best Sellers Rank', -1 ],
            [ 'Date first listed on Amazon', -1 ],
            [ 'Date First Available', -1 ],
            [ 'Warranty & Support', -1 ],
            [ 'Technical Specification', -1 ],
            [ 'Customer Reviews', -1 ],
            [ 'Operating System', -1 ],
            [ 'Feedback', -1 ],
            [ 'Manufacturer Part Number', -1 ],
            [ 'Color', -1 ],
            [ 'Number of Items', -1 ],
            [ 'Technical Details', -1 ],
            [ 'Additional Information', -1 ],
            [ 'National Stock Number', -1 ],
        ]

        productInformation = self.__response.get('productInformation')

        if type(productInformation) is str:
            informationDict = self.__fillSearchTerms(productInformation, searchTerms)

            self.__stuffClassFromInfoDict(informationDict)

    def __stuffClassFromInfoDict(self, informationDict):
        self.__asin = informationDict.get("ASIN")
        self.__model = informationDict.get("Item model number")
        self.__shippingWeight = informationDict.get('Shipping Weight')
        self.__itemWeight = informationDict.get("Item Weight")
        self.__bestSellersRank = informationDict.get('Best Sellers Rank')
        self.__dateFirstListed = informationDict.get('Date first listed on Amazon')

    def __fillSearchTerms(self, productInformation, searchTerms):
        """
        Given the product information string and the search terms multi dimensional list go through the search terms and populate the values based on the information in the product string.
        """
        informationDict = {}

        for term in searchTerms:
            term[1] = productInformation.find(term[0])

        searchTerms.sort(key=lambda x: x[1])

        for i in range(len(searchTerms)):
            term = searchTerms[i]

            # find the end of the value we're looking for. It's either the start of the next term or the end of the string
            if i < (len(searchTerms) - 1):
                end = searchTerms[i + 1][1] - 1
            else:
                end = -1

            if term[1] != -1:
                start = term[1] + len(term[0]) + 1
                val = productInformation[start : end]
                informationDict.update({term[0]: val})
        
        return informationDict

    def __fillDict(self):
        productDict = {}
        properties = dir(self)

        for prop in properties:
            if prop[0] != '_':
                value = self.__getattribute__(prop)
                if not inspect.ismethod(value):
                    productDict.update({prop: self.__getattribute__(prop)})
        
        self.productDict = productDict # do this here so things don't get self referenced...

    def __getPrice(self):
        try:
            priceList = self.__response.get("Price").split("$")
            if len(priceList) >= 1:
                priceString = priceList[1]
                price = priceString.split(',')
                cleanPrice = ''.join(price)
                self.__price = float(cleanPrice)
        except:
            print("Can't parse %s"%self.__response.get("Price"))

    def printItem(self):
        print("Product Name: %s"%self.__productName)
        print("Price: %s"%self.__price)
        print("URL: %s"%self.__itemURL)
        print("Product Type: %s"%self.__productType)
        print("Product Category: %s"%self.__productCategory)
        print("Availability: %s"%self.__availability)
        print("Category Rank: %s"%self.__categoryRank)



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
