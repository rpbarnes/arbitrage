from base_item import baseItem
import inspect

class ebayItem():
    def __init__(self, response):
        self.__baseItem = baseItem()
        self.__response = response
        self.__itemURL = response.get('viewItemURL')

    def parseData(self, extractedHtml):
        self.__extractedHtml = extractedHtml
        self.__title = self.__response.get("title")
        self.__itemURL = self.__response.get("viewItemURL")
        self.__location = self.__response.get("location")
        self.__shippingCost = self.__response.get("shippingType")
        self.__buyNow = self.__response.get("listingInfo")
        self.__getProductCategory()
        self.__getProductPrice()
        self.__getCondition()
        self.__parseProductInformation()
        self.__fillDict()


    @property
    def condition(self):
        return self.__condition

    @property
    def category(self):
        return self.__category

    @property
    def price(self):
        return self.__price

    @property
    def currency(self):
        return self.__currency

    @property
    def buyNow(self):
        return self.__buyNow

    @property
    def shippingCost(self):
        return self.__shippingCost

    @property
    def locationn(self):
        return self.__location

    @property
    def title(self):
        return self.__title

    @property
    def model(self):
        return self.__model

    @property
    def brand(self):
        return self.__brand

    @property
    def itemURL(self):
        return self.__itemURL

    @property
    def mpn(self):
        return self.__mpn

    def __parseProductInformation(self):
        """
        Parse product string information.

        Given a list of search terms. Look for those terms in the product information string. find the position of those terms. then go through the product information string, given position of indecies, and pull out necessary product information.
        """
        searchTerms = [
            [ 'Condition:', -1 ],
            [ 'MPN:', -1 ],
            [ 'Brand:', -1 ],
            [ 'UPC:', -1 ],
            [ 'Model:', -1 ],
            [ 'Material:', -1 ],
            [ 'Dimensions:', -1 ],
            [ 'Manufacturer:', -1 ],
            [ 'GTIN:', -1 ],
            [ 'Interface:', -1 ],
            [ 'Weight:', -1 ],
            [ 'Country/Region of Manufacture:', -1 ],
            [ 'Type:', -1 ],
            [ 'Interface:', -1 ],
            [ 'Handset Type:', -1 ],
            [ 'Features:', -1 ],
            [ 'Custom Bundle:', -1 ],
            [ 'Modified Item:', -1 ],
            [ 'Bundle Listing:', -1 ],
            [ 'Network:', -1 ],
            [ 'Storage Capacity:', -1 ],
            [ 'Manufacturer Warranty:', -1 ],
            [ 'Processor:', -1 ],
            [ 'Screen Size:', -1 ],
            [ 'Camera Resolution:', -1 ],
            [ 'Operating System:', -1 ],
            [ 'Contract:', -1 ],
            [ 'Model Number:', -1 ],
            [ 'Lock Status:', -1 ],
            [ 'Memory Card Type:', -1 ],
            [ 'Manufacturer Color:', -1 ],
            [ 'Style:', -1 ],
            [ 'Cellular Band:', -1 ],
            [ 'Connectivity:', -1 ],
            [ 'RAM:', -1 ],
            [ 'Output Type:', -1 ],
            [ 'Application:', -1 ],
            [ 'Interior Dimensions:', -1 ],
            [ 'Color:', -1 ],
            [ 'Size:', -1 ],
            [ 'Number of Shelves:', -1 ],
            [ 'Custom Label:', -1 ],
            [ 'Height:', -1 ],
            [ 'Processor Speed:', -1 ],
            [ 'Processor Type:', -1 ],
            [ 'Processor Manufacturer:', -1 ],
            [ 'RAID Levels:', -1 ],
            [ '10GB Capability:', -1 ],
            [ 'Generation:', -1 ],
            [ 'Non-Domestic Product:', -1 ],
            [ 'Form Factor:', -1 ],
            [ 'Number of Processors:', -1 ],
            [ 'Memory (RAM) Capacity:', -1 ],
            [ 'Memory Type:', -1 ],

            [ 'Product Line:', -1 ],
            [ 'Recordable Disc Formats:', -1 ],
            [ 'Playable File Formats:', -1 ],
            [ 'Playable Disk Formats:', -1 ],
        ]

        productInformation = self.__extractedHtml.get('itemSpecificsString')

        if type(productInformation) is str:
            informationDict = self.__baseItem.fillSearchTerms(productInformation, searchTerms)

            self.__stuffClassFromInfoDict(informationDict)

    def __stuffClassFromInfoDict(self, informationDict):
        self.__model = informationDict.get("Model:")
        self.__brand = informationDict.get("Brand:")
        self.__mpn = informationDict.get("MPN:")


    def __fillDict(self):
        """ Fills dictionary of all values of the class should be run last.
        """
        productDict = {}
        properties = dir(self)

        for prop in properties:
            if prop[0] != '_':
                value = self.__getattribute__(prop)
                if not inspect.ismethod(value):
                    productDict.update({prop: self.__getattribute__(prop)})
        
        self.productDict = productDict # do this here so things don't get self referenced...

    def __getCondition(self):
        self.__condition = None

        conditionString = self.__response.get("condition")

        if (conditionString != None):
            self.__condition = conditionString.get("conditionDisplayName")

    def __getProductCategory(self):
        self.__category = None

        categoryString = self.__response.get("primaryCategory")

        if (categoryString != None):
            self.__category = categoryString.get("categoryName")

    
    def __getProductPrice(self):
        self.__price = None
        self.__currency = None
        priceString = self.__response.get("sellingStatus")

        if (priceString != None):
            currentPrice = priceString.get("currentPrice")

            if (currentPrice != None):
                try:
                    self.__currency = currentPrice.get("currencyId")
                    self.__price = float(currentPrice.get("value"))
                except:
                    print("Cannot parse price")



    def printItem(self):
        print("Title: %s"%self.title)
        print("Category: %s"%self.category)
        print("URL: %s"%self.itemURL)
        print("Shipping Cost: %s"%self.shippingCost)
        print("Price: %s"%self.price)
        print("Brand: %s"%self.brand)
        print("Model: %s"%self.model)
        print("Buy Now: %s"%self.buyNow)
        print("Condition: %s"%self.condition)