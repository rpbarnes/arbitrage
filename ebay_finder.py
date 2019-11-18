import datetime
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
from selectorlib import Extractor
from scraper_agent import scraperAgent
import re
import json
from ebay_item import ebayItem

# ebay finding sdk documentation
# https://developer.ebay.com/Devzone/finding/CallRef/findItemsAdvanced.html


# the get item information needs improvement to actually get the item info
class EbayFinder():
    def __init__(self):
        self._apiKey = 'RyanBarn-listalle-PRD-2b31f1040-dd93d724'
        self._api = Connection(appid=self._apiKey, config_file=None)
        self._agent = scraperAgent()
        self._productExtractor = Extractor.from_yaml_file('selectors/EbayProductSelection2.yml')

    def findItemsByKeyword(self, searchWords, page = 1):
        response = self._api.execute('findItemsAdvanced', {
            'keywords': searchWords, 
            #'sortOrder': 'PricePlusShippingHighest', 
            'page': page,
            #'paginationOutput':{'entriesPerPage': 500, 'pageNumber': page}, # this command doesn't work...
            })
        return [ebayItem(x) for x in response.reply.searchResult.item]

    def getItemInformation(self, ebayItem):
        html = self._agent.getHtmlContent(ebayItem.itemURL)
        data = self._productExtractor.extract(html.text)

        ebayItem.parseData(data)


        return ebayItem








if __name__ == "__main__":
    ebay = EbayFinder()

    listOfItems = ebay.findItemsByKeyword("conference equipment new")

    #for item in listOfItems:
    #    data = ebay.getItemInformation(item)
    #    data.printItem()

    #    print('\n\n')
    #    print(json.dumps(data.itemSpecifics, indent=4, skipkeys=True))
    #    print('\n\n')

    #    next = input("press for next")
    #    print('\n\n')

    listOfItems2 = ebay.findItemsByKeyword("cisco microphone new", page=12)

    data1 = ebay.getItemInformation(listOfItems[-1])
    data2 = ebay.getItemInformation(listOfItems2[-1])

    data1.printItem()
    data2.printItem()


