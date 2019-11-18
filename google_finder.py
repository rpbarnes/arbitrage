from googlesearch import search

class googleFinder():
    def __init__(self):
        self.query = ''

    def search(self, query, numResults=5):
        return search(query, tld='com', num=numResults)
