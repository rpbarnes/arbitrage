
import inspect
from base_item import baseItem

class amazonItem():
    def __init__(self, response):
        self.__response = response
        self.__initializeClass()
        self.__baseItem = baseItem()
    
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
            informationDict = self.__baseItem.fillSearchTerms(productInformation, searchTerms)

            self.__stuffClassFromInfoDict(informationDict)

    def __stuffClassFromInfoDict(self, informationDict):
        self.__asin = informationDict.get("ASIN")
        self.__model = informationDict.get("Item model number")
        self.__shippingWeight = informationDict.get('Shipping Weight')
        self.__itemWeight = informationDict.get("Item Weight")
        self.__bestSellersRank = informationDict.get('Best Sellers Rank')
        self.__dateFirstListed = informationDict.get('Date first listed on Amazon')


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
