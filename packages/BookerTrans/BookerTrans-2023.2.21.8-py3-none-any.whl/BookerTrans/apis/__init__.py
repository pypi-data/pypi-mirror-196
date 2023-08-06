from .GoTransSeleniumApi import GoTransSeleniumApi
from .BaiTransSeleniumApi import BaiTransSeleniumApi
from .AliTransSeleniumApi import AliTransSeleniumApi
from .BingTransSeleniumApi import BingTransSeleniumApi
from .SoTransSeleniumApi import SoTransSeleniumApi
from .YoudaoTransSeleniumApi import YoudaoTransSeleniumApi
from .YoudaoTransApi import YoudaoTransApi
from .QTransSeleniumApi import QTransSeleniumApi
from .DeeplTransSeleniumApi import DeeplTransSeleniumApi

apis = {
    'google_selenium': GoTransSeleniumApi,
    'ali_selenium': AliTransSeleniumApi,
    'bing_selenium': BingTransSeleniumApi,
    'baidu_selenium': BaiTransSeleniumApi,
    'sogou_selenium': SoTransSeleniumApi,
    'youdao': YoudaoTransApi,
    'youdao_selenium': YoudaoTransSeleniumApi,
    'qq_selenium': QTransSeleniumApi,
    'deepl': DeeplTransSeleniumApi,
}