
url = r"http://svcs.ebay.com/services/search/FindingService/v1"
url += r"?OPERATION-NAME=findItemsByKeywords"
url += r"&SERVICE-VERSION=1.0.0"
url += r"&SECURITY-APPNAME=MyAppID"
url += r"&GLOBAL-ID=EBAY-US"
url += r"&RESPONSE-DATA-FORMAT=JSON"
url += r"&callback=_cb_findItemsByKeywords"
url += r"&REST-PAYLOAD"
url += r"&keywords=harry%20potter"
url += r"&paginationInput.entriesPerPage=3"
url += r"&SECURITY-APPNAME=RyanBarn-listalle-PRD-2b31f1040-dd93d724"


print(url)
