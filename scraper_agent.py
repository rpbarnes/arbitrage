import requests

class scraperAgent():
    def __init__(self):
        self.user_agent_pool = ['Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev>(KHTML, like Gecko) Chrome/<Chrome Rev> Safari/<WebKit Rev>', 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36']
        #user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'

        self.user_agent_count = 0


    def getHtmlContent(self, url):

        headers = { 'User-Agent': self.user_agent_pool[self.user_agent_count] }

        return requests.get(url, headers=headers)

    def switchUserAgent(self):
        self.user_agent_count += 1
        if self.user_agent_count > (len(self.user_agent_pool) - 1):
            self.user_agent_count = 0
