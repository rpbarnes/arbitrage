from amazon_product_finder import amazonFinder, amazonItem
import unittest

class Test_amazon_product_finder(unittest.TestCase):
    
    def test_parse_price(self):
        item = amazonItem({'Price':'$1,000,000'})
        self.assertEqual(1000000.0, item.price, "Price is not properly parsed.")
        self.assertEqual(1000000.0, item.productDict.get('priceAmazon'), "Price is not properly parsed.")





if __name__ == '__main__':
    unittest.main()