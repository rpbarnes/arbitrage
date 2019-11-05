from ebay_finder import EbayFinder
from amazon_product_finder import amazonFinder
from csv_write import CsvWriter

searchTerms = ["networking equipment new", "electronics new"]

ebay = EbayFinder()
amazon = amazonFinder()
csvWriter = CsvWriter()

for searchTerm in searchTerms:

    for page in range(5):

        ebayProducts = ebay.findItemsByKeyword(searchTerm, page=page)

        for ebayProduct in ebayProducts:

            ebayProduct = ebay.getItemInformation(ebayProduct)

            ebayProduct.printItem()
            print(ebayProduct.productData)

            if (ebayProduct.brand != "" and ebayProduct.model != "" and ebayProduct.condition == "New"):
                amazonProduct = amazon.findBestMatch(keywords="%s %s"%(ebayProduct.brand, ebayProduct.model))

                if (amazonProduct != None):
                    amazonProduct.printItem()

                    csvWriter.write(amazonProduct, ebayProduct)

            else:
                print("Invalid product")


            print("Running next search")



