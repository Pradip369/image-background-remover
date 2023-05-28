# from django.test import TestCase

# Create your tests here.

import requests

url = 'http://127.0.0.1:8000/api/remove_bg/fast_remove/'
myobj = {'somekey': 'somevalue'}
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

x = requests.post(url, data = myobj)

print(x.text)