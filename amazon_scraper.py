from selectorlib import Extractor
import requests
import json
import argparse

associateID = 'technolog0ed0-20'

argparser = argparse.ArgumentParser()
argparser.add_argument('url', help='Amazon Product Details URL')

# create an extractor for the downloaded html content
e = Extractor.from_yaml_file('selectors/amazon.yml')

user_agent = 'Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev>(KHTML, like Gecko) Chrome/<Chrome Rev> Safari/<WebKit Rev>'
#user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
headers = { 'User-Agent': user_agent }

# download the page using requests
args = argparser.parse_args()
r = requests.get(args.url, headers=headers)

# pass the html content 
data = e.extract(r.text)

#print(r.text)

print(json.dumps(data, indent=True))
