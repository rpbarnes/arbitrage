from ebay_item import ebayItem
import unittest

class Test_ebay_item(unittest.TestCase):

    def test_parse_product_information(self):
        dic = {'itemSpecificsString': 'Item specifics Condition: New: A brand-new, unused, unopened, undamaged item in its original packaging (where packaging is ... Read more about the condition Model: 5303 MPN: 50001900 Country/Region of Manufacture: Canada Brand: Mitel Type: Audio Conferencing UPC: Does not apply'}
        item = ebayItem(dic)
        item.parseData('')
        self.assertEqual('5303', item.model)
        self.assertEqual('Mitel', item.brand)