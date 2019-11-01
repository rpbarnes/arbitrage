import datetime
from .ebaysdk.exception import ConnectionError
from .ebaysdk.finding import Connection


class EbayItem():
    def __init__(self, response):
        self.Title = response.get("title")
        self.Category = response.get("primaryCategory")
        self.ItemURL = response.get("viewItemURL")
        self.Location = response.get("location")
        self.shippingCost = response.get("shippingType")
        self.price = response.get("sellingStatus")
        self.buyNow = response.get("listingInfo")
        self.condition = response.get("condition")

    def printItem(self):
        print("Title: %s"%self.Title)
        print("Category: %s"%self.Category)
        print("URL: %s"%self.ItemURL)
        print("Location: %s"%self.Location)
        print("Shipping Cost: %s"%self.shippingCost)
        print("Price: %s"%self.price)
        print("Buy Now: %s"%self.buyNow)
        print("Condition: %s"%self.condition)

key = 'RyanBarn-listalle-PRD-2b31f1040-dd93d724'
try:
    api = Connection(appid=key, config_file=None)
    response = api.execute('findItemsAdvanced', {'keywords': 'cisco', "condition": 1000})

    for item in response.reply.searchResult.item:
        ebayItem = EbayItem(item)
        #ebayItem.printItem()
        print(ebayItem.condition)

    



except ConnectionError as e:
    print(e)
    print(e.response.dict())


