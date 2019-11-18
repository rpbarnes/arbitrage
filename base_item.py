

class baseItem():

    def fillSearchTerms(self, productInformation, searchTerms):
        """
        Given the product information string and the search terms multi dimensional list go through the search terms and populate the values based on the information in the product string.
        """
        informationDict = {}

        for term in searchTerms:
            term[1] = productInformation.find(term[0])

        searchTerms.sort(key=lambda x: x[1])

        for i in range(len(searchTerms)):
            term = searchTerms[i]

            # find the end of the value we're looking for. It's either the start of the next term or the end of the string
            if i < (len(searchTerms) - 1):
                end = searchTerms[i + 1][1] - 1
            else:
                end = -1

            if term[1] != -1:
                start = term[1] + len(term[0]) + 1
                val = productInformation[start : end]
                informationDict.update({term[0]: val})
        
        return informationDict
