from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import sys
from .SeleniumApi import SeleniumApi

class DeeplTransSeleniumApi(SeleniumApi):

    def get_settings(self):
        return {
            'default_url': 'https://www.deepl.com/translator#en/zh-CN/',
            'url_temp': 'https://www.deepl.com/translator#{src}/{dst}/',
            'src_sel': '.lmt__source_textarea',
            'src_attr': 'value',
            'dst_sel': '.lmt__target_textarea',
            'dst_attr': 'value',
        }
        
    def translate(self, s, src='en', dst='zh'):
        if src == 'auto': src = 'en'
        if dst == 'zh-CN': dst = 'zh'
        return SeleniumApi.translate(self, s, src, dst)

def main():
    api = DeeplTransSeleniumApi()
    print(api.translate(sys.argv[1]))
    
if __name__ == '__main__': main()