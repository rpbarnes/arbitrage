import datetime
from ebaysdk_local.exception import ConnectionError
from ebaysdk_local.finding import Connection
from selectorlib import Extractor
from scraper_agent import scraperAgent
import re

# ebay finding sdk documentation
# https://developer.ebay.com/Devzone/finding/CallRef/findItemsAdvanced.html

class EbayItem():
    def __init__(self, response):
        self._response = response
        self.initializeDict()
        self.brand = ""
        self.model = ""
        self.title = response.get("title")
        self.productDict.update({'titleEbay': self.title})
        self.getProductCategory()
        self.itemURL = response.get("viewItemURL")
        self.productDict.update({'itemURLEbay': self.itemURL})
        self.location = response.get("location")
        self.productDict.update({'locationEbay': self.location})
        self.shippingCost = response.get("shippingType")
        self.productDict.update({'shippingCostEbay': self.shippingCost})
        self.getProductPrice()
        self.buyNow = response.get("listingInfo")
        self.getCondition()

    def initializeDict(self):
        self.productDict = {}
        self.productDict.update({'titleEbay': ""})
        self.productDict.update({'itemURLEbay': ""})
        self.productDict.update({'locationEbay': ""})
        self.productDict.update({'shippingCostEbay': ""})
        self.productDict.update({'conditionEbay': ""})
        self.productDict.update({'categoryEbay': ""})
        self.productDict.update({'priceEbay': ""})
        self.productDict.update({'currencyEbay': ""})

    def getCondition(self):
        self.condition = None

        conditionString = self._response.get("condition")

        if (conditionString != None):
            self.condition = conditionString.get("conditionDisplayName")
            self.productDict.update({'conditionEbay': self.condition})

    def getProductCategory(self):
        self.category = None

        categoryString = self._response.get("primaryCategory")

        if (categoryString != None):
            self.category = categoryString.get("categoryName")
            self.productDict.update({'categoryEbay': self.category})


    
    def getProductPrice(self):
        self.price = None
        self.currency = None

        priceString = self._response.get("sellingStatus")

        if (priceString != None):
            currentPrice = priceString.get("currentPrice")

            if (currentPrice != None):
                try:
                    self.currency = currentPrice.get("currencyId")
                    self.price = float(currentPrice.get("value"))
                    self.productDict.update({'priceEbay': self.price})
                    self.productDict.update({'currencyEbay': self.currency})
                except:
                    self.price = None



    def printItem(self):
        print("Title: %s"%self.title)
        print("Category: %s"%self.category)
        print("URL: %s"%self.itemURL)
        print("Location: %s"%self.location)
        print("Shipping Cost: %s"%self.shippingCost)
        print("Price: %s"%self.price)
        print("Brand: %s"%self.brand)
        print("Model: %s"%self.model)
        print("Buy Now: %s"%self.buyNow)
        print("Condition: %s"%self.condition)

class EbayFinder():
    def __init__(self):
        self._apiKey = 'RyanBarn-listalle-PRD-2b31f1040-dd93d724'
        self._api = Connection(appid=self._apiKey, config_file=None)
        self._agent = scraperAgent()
        self._productExtractor = Extractor.from_yaml_file('selectors/EbayProductSelection2.yml')

    def findItemsByKeyword(self, searchWords, page = 1):
        response = self._api.execute('findItemsAdvanced', {
            'keywords': searchWords, 
            'sortOrder': 'PricePlusShippingHighest', 
            'paginationOutput':{'entriesPerPage': 500, 'pageNumber': page},
            
            })
        return [EbayItem(x) for x in response.reply.searchResult.item]

    def getItemInformation(self, ebayItem):
        html = self._agent.getHtmlContent(ebayItem.itemURL)
        data = self._productExtractor.extract(html.text)

        ebayItem.brand = data.get('Brand2')
        ebayItem.productData = data

        ebayItem = self.fillInModelData(ebayItem, data)

        return ebayItem

    def fillInModelData(self, ebayItem, data):

        fieldsToCheck = ['MPN2', 'Model2', 'Model3', 'MPN',  'Model']

        # look for the first that contains a number
        for fieldToCheck in fieldsToCheck:
            toCheck = data.get(fieldToCheck)

            if type(toCheck) is str:

                match = re.search(r'\d', toCheck)

                if (match != None): # see if it looks like a part number
                    ebayItem.model = toCheck
                    print("taking %s"%toCheck)
                    break

        return ebayItem







if __name__ == "__main__":
    ebay = EbayFinder()

    listOfItems = ebay.findItemsByKeyword("cisco microphone new")

    #for item in listOfItems:
    #    data = ebay.getItemInformation(item)
    #    data.printItem()
    #    print(data.productData)
    #    next = input("press for next")

    listOfItems2 = ebay.findItemsByKeyword("cisco microphone new", page=12)

    data1 = ebay.getItemInformation(listOfItems[-1])
    data2 = ebay.getItemInformation(listOfItems2[-1])

    data1.printItem()
    data2.printItem()


