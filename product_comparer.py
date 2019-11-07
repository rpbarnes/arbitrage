from ebay_finder import EbayFinder
from amazon_product_finder import amazonFinder
from csv_write import CsvWriter
import time

searchTerms = ["cisco microphone new", "lot office phone new", "textbook new" ]

ebay = EbayFinder()
amazon = amazonFinder()
csvWriter = CsvWriter(filename=time.strftime("%Y%m%d-%H%M%S") + "_results.csv")

for searchTerm in searchTerms:

    for page in range(1):

        ebayProducts = ebay.findItemsByKeyword(searchTerm, page=page)

        for ebayProduct in ebayProducts:

            if (ebayProduct.price > 10):
                ebayProduct = ebay.getItemInformation(ebayProduct)

                ebayProduct.printItem()
                print(ebayProduct.productData)

                if (ebayProduct.brand != "" and ebayProduct.model != "" and ebayProduct.condition == "New"):
                    amazonProduct = amazon.findBestMatch(keywords="%s %s"%(ebayProduct.brand, ebayProduct.model))

                    if (amazonProduct != None):
                        amazonProduct.printItem()

                        csvWriter.write(amazonProduct, ebayProduct)

                else:
                    print("Invalid product, sleeping for time.") 
                    time.sleep(2)

            else:
                print("Price is too low skipping")

            print("Running next search")



