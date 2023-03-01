# -*- coding: utf-8 -*-

import webbrowser
import requests, html
import clipboard

from wox import Wox


HEADERS = {'Host': 'apis.dict.cn', 'Referer': 'http://dict.cn/'}
API_ADDR = "http://apis.dict.cn/apis/suggestion.php"
WEB_ADDR = "http://dict.cn/search"

class Dictionary(Wox):
    def request(self, url, params):

        #If user set the proxy, you should handle it.
        if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
            proxies = {
                "http":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port")),
                "https":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port"))}
            return requests.get(url, params=params, headers=HEADERS, proxies=proxies)
        else:
            return requests.get(url, params=params, headers=HEADERS)

    def query(self, query):
        results = []
        if not query:
            results.append({
                "Title": "英/汉词语",
                "SubTitle": "从 http://dict.cn 获取英汉词语解释",
                "IcoPath":"Images/translate.png",
            })
            return results
        
        data = self.request(API_ADDR,  {"lt": "zh-cn", "q": query}).json()

        explains = data.get("s")

        if not explains:
            results.append({
                "Title": "找不到对应的翻译",
                "SubTitle": "从 http://dict.cn 获取英汉词语解释",
                "IcoPath":"Images/translate.png",
            })
            return results

        for d in explains:
            results.append({
                "Title": d.get("g").lstrip(),
                "SubTitle": html.unescape(d.get("e")).lstrip(),
                "IcoPath":"Images/translate.png",
                "ContextData": "ctxData",
                "JsonRPCAction": {
                    'method': 'open_browser',
                    'parameters': ["{}?q={}".format(WEB_ADDR, d.get("g"))],
                    'dontHideAfterAction': False
                }
             })
        return results

    # context_menu is default function called for ContextData where `data = ctxData`
    def context_menu(self, data):
        results = []
        results.append({
            "Title": "Context menu entry",
            "SubTitle": "Data: {}".format(data),
            "IcoPath":"Images/translate.png"
        })
        return results

    def copy(self, text):
        clipboard.copy(text)

    def open_browser(self, url):
        webbrowser.open(url)
        

if __name__ == "__main__":
    Dictionary()
