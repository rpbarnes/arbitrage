import requests

class scraperAgent():
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev>(KHTML, like Gecko) Chrome/<Chrome Rev> Safari/<WebKit Rev>'
        #user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
        self.headers = { 'User-Agent': self.user_agent }

    def getHtmlContent(self, url):
        return requests.get(url, headers=self.headers)