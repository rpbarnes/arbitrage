from urllib.parse import urljoin
from selectorlib import Extractor
from googlesearch import search
from scraper_agent import scraperAgent
import itertools
import json
import time


class googleFinder():
    def __init__(self):
        self.query = ''

    def search(self, query, numResults=5):
        return search(query, tld='com', num=numResults)


class amazonItem():
    def __init__(self, response):
        self._response = response
        self.initializeDict()
        self.itemURL = ""
        self.getPrice()
        self.productName = response.get("ProductName")
        self.productDict.update({"productNameAmazon": self.productName})
        self.productType = response.get("ProductType")
        self.productDict.update({"productTypeAmazon": self.productType})
        self.productCategory = response.get("ProductCategory")
        self.productDict.update({"productCategoryAmazon": self.productCategory})
        self.availability = response.get("Availability")
        self.productDict.update({"availabilityAmazon": self.availability})
        self.categoryRank = response.get("CategoryRank")
        self.productDict.update({"categoryRankAmazon": self.categoryRank})

    def initializeDict(self):
        self.productDict = {}
        self.productDict.update({"productNameAmazon": ""})
        self.productDict.update({"itemURLAmazon": ""})
        self.productDict.update({"productTypeAmazon": ""})
        self.productDict.update({"productCategoryAmazon": ""})
        self.productDict.update({"availabilityAmazon": ""})
        self.productDict.update({"categoryRankAmazon": ""})
        self.productDict.update({"priceAmazon": ""})
    
    def getPrice(self):
        self.price = None

        try:
            priceList = self._response.get("Price").split("$")
            if len(priceList) >= 1:
                self.price = float(priceList[1])
                self.productDict.update({"priceAmazon": self.price})
        except:
            print("Can't parse %s"%self._response.get("Price"))

    def printItem(self):
        print("Product Name: %s"%self.productName)
        print("Price: %s"%self.price)
        print("URL: %s"%self.itemURL)
        print("Product Type: %s"%self.productType)
        print("Product Category: %s"%self.productCategory)
        print("Availability: %s"%self.availability)
        print("Category Rank: %s"%self.categoryRank)



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
        print("searching for %s..."%keywords)

        results = self._google.search(keywords + ' amazon')

        searchFilters = keywords.split(' ')

        count = 0
        for result in results:

            if ('www.amazon' in result):
                productData = self.extractAmazonProductInfo(result)

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
                    item.itemURL = result
                    item.productDict.update({"itemURLAmazon": result})
                    return item

            if (count > num_results):
                return None

            count += 1




#google = googleFinder()
#
#result = google.search('cisco SG350-28P-K9 amazon')
#
#print(result)

if __name__ == "__main__":
    amazon = amazonFinder()

    productData = amazon.findBestMatch(keywords='cisco SG350')

    productData.printItem()
