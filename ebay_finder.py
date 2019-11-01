import datetime
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection


class EbayItem():
    def __init__(self, response):
        self._response = response
        self.title = response.get("title")
        self.getProductCategory()
        self.itemURL = response.get("viewItemURL")
        self.location = response.get("location")
        self.shippingCost = response.get("shippingType")
        self.getProductPrice()
        self.buyNow = response.get("listingInfo")
        self.condition = response.get("condition")

    def getProductCategory(self):
        self.category = None

        categoryString = self._response.get("primaryCategory")

        if (categoryString != None):
            self.category = categoryString.get("categoryName")


    
    def getProductPrice(self):
        self.price = None
        self.currency = None

        priceString = self._response.get("sellingStatus")

        if (priceString != None):
            currentPrice = priceString.get("currentPrice")

            if (currentPrice != None):
                self.price = currentPrice.get("value")
                self.currency = currentPrice.get("currencyId")


    def printItem(self):
        print("Title: %s"%self.title)
        print("Category: %s"%self.category)
        print("URL: %s"%self.itemURL)
        print("Location: %s"%self.location)
        print("Shipping Cost: %s"%self.shippingCost)
        print("Price: %s"%self.price)
        print("Buy Now: %s"%self.buyNow)
        print("Condition: %s"%self.condition)

key = 'RyanBarn-listalle-PRD-2b31f1040-dd93d724'
try:
    api = Connection(appid=key, config_file=None)
    response = api.execute('findItemsAdvanced', {'keywords': 'mitel new'})

    ebayItem = EbayItem(response.reply.searchResult.item[0])
    ebayItem.printItem()
    #for item in response.reply.searchResult.item:
    #    ebayItem = EbayItem(item)
    #    ebayItem.printItem()
    #    #print(ebayItem.condition)

    



except ConnectionError as e:
    print(e)
    print(e.response.dict())


