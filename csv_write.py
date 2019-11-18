import csv
from amazon_product_finder import amazonItem
from ebay_item import ebayItem
import os.path

class CsvWriter():
    def __init__(self, filename = "results.csv"):
        self._filename = filename
        self._writer = None


    def write(self, amazonItem, ebayItem):
        """
        Open file write item value and close file

        Takes dictionary objects from each type. Concatenates them and writes to file
        """
        towrite = None
        if (amazonItem != None and ebayItem != None):
            towrite = amazonItem.productDict
            if (towrite != None):
                towrite.update(ebayItem.productDict)

        if (towrite != None):
            if (self._writer == None):
                self._csvfile = open(self._filename, mode='w')
                self._writer = csv.DictWriter(self._csvfile, fieldnames=towrite.keys())
                self._writer.writeheader()

            self._writer.writerow(towrite)




