# -*- coding: utf-8 -*-

import webbrowser
import requests, html, json
import clipboard

from wox import Wox

class Dictionary(Wox):
    def request(self, url, params):
        headers = {'Host': 'apis.dict.cn', 'Referer': 'http://dict.cn/'}

        #If user set the proxy, you should handle it.
        if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
            proxies = {
                "http":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port")),
                "https":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port"))}
            return requests.get(url, params=params, headers=headers, proxies=proxies)
        else:
            return requests.get(url, params=params, headers=headers)

    def query(self, query):
        results = []
        if not query:
            results.append({
                "Title": "英/汉词语",
                "SubTitle": "从 http://dict.cn 获取英汉词语解释",
                "IcoPath":"Images/translate.png",
            })
            return results
        
        data = self.request("http://apis.dict.cn/apis/suggestion.php",  {"lt": "zh-cn", "q": query}).json()

        for d in data.get("s"):
            results.append({
                "Title": "{}".format(d.get("g")),
                "SubTitle": "{}".format(html.unescape(d.get("e"))),
                "IcoPath":"Images/translate.png",
                "ContextData": "ctxData",
                "JsonRPCAction": {
                    'method': 'open_browser',
                    'parameters': ["http://dict.cn/search?q={}".format(d.get("g"))],
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
