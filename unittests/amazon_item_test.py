from amazon_product_finder import amazonFinder, amazonItem
import unittest

class Test_amazon_item(unittest.TestCase):
    
    def test_parse_price(self):
        item = amazonItem({'Price':'$1,000,000'})
        item.parseData('')
        self.assertEqual(1000000.0, item.price, "Price is not properly parsed.")
        self.assertEqual(1000000.0, item.productDict.get('price'), "Price is not properly parsed.")

    def test_parse_product_information(self):
        dic = {'productInformation': 'Product information Product Dimensions 7.4 x 5.9 x 1.9 inches Item Weight 0.16 ounces Shipping Weight 6.6 ounces (View shipping rates and policies) ASIN B01N2ZKOPA Item model number CTS-MIC-TABL60= Best Sellers Rank #13,195 in Telephones Date first listed on Amazon May 19, 2015 Warranty & Support Product Warranty: For warranty information about this product, please click here Feedback If you are a seller for this product, would you like to suggest updates through seller support? Would you like to tell us about a lower price?'}
        item = amazonItem(dic)
        item.parseData('')
        self.assertEqual('B01N2ZKOPA', item.asin)
        self.assertEqual('CTS-MIC-TABL60=', item.model)
        self.assertEqual('6.6 ounces (View shipping rates and policies)', item.shippingWeight)
        self.assertEqual('0.16 ounces', item.itemWeight)
        self.assertEqual('#13,195 in Telephones', item.bestSellersRank)
        self.assertEqual('May 19, 2015', item.dateFirstListed)

    def test_parse_product_information1(self):
        dic = {'productInformation': '"Product information Style:Meeting Owl (Camera Only) Product Dimensions 4.4 x 4.4 x 10.8 inches Item Weight 2.65 pounds Shipping Weight 4.9 pounds (View shipping rates and policies) ASIN B075X1VL3Y Item model number MTW100 Customer Reviews 4.2 out of 5 stars 136 ratings 4.2 out of 5 stars Best Sellers Rank #769 in Amazon Launchpad (See Top 100 in Amazon Launchpad) #10 in Amazon Launchpad Camera #48 in Webcams Date first listed on Amazon September 25, 2017 Technical Specification Specification Sheet [pdf ] Warranty & Support Manufacturer’s warranty can be requested from customer service. Click here to make a request to customer service. Feedback If you are a seller for this product, would you like to suggest updates through seller support? Would you like to tell us about a lower price?"'}
        item = amazonItem(dic)
        item.parseData('')
        self.assertEqual('B075X1VL3Y', item.asin)
        self.assertEqual('MTW100', item.model)
        self.assertEqual('4.9 pounds (View shipping rates and policies)', item.shippingWeight)
        self.assertEqual('2.65 pounds', item.itemWeight)
        self.assertEqual('#769 in Amazon Launchpad (See Top 100 in Amazon Launchpad) #10 in Amazon Launchpad Camera #48 in Webcams', item.bestSellersRank)
        self.assertEqual('September 25, 2017', item.dateFirstListed)


    def test_item_converts_to_dict(self):
        dic = {'productInformation': '"Product information Style:Meeting Owl (Camera Only) Product Dimensions 4.4 x 4.4 x 10.8 inches Item Weight 2.65 pounds Shipping Weight 4.9 pounds (View shipping rates and policies) ASIN B075X1VL3Y Item model number MTW100 Customer Reviews 4.2 out of 5 stars 136 ratings 4.2 out of 5 stars Best Sellers Rank #769 in Amazon Launchpad (See Top 100 in Amazon Launchpad) #10 in Amazon Launchpad Camera #48 in Webcams Date first listed on Amazon September 25, 2017 Technical Specification Specification Sheet [pdf ] Warranty & Support Manufacturer’s warranty can be requested from customer service. Click here to make a request to customer service. Feedback If you are a seller for this product, would you like to suggest updates through seller support? Would you like to tell us about a lower price?"'}
        item = amazonItem(dic)
        item.parseData('')
        self.assertEqual(item.productDict.get('asin'), item.asin)
        self.assertEqual(item.productDict.get('model'), item.model)
        self.assertEqual(item.productDict.get('shippingWeight'), item.shippingWeight)
        self.assertEqual(item.productDict.get('itemWeight'), item.itemWeight)
        self.assertEqual(item.productDict.get('bestSellersRank'), item.bestSellersRank)
        self.assertEqual(item.productDict.get('dateFirstListed'), item.dateFirstListed)


if __name__ == '__main__':
    unittest.main()