import logging
import requests, time, json
from requests.cookies import cookiejar_from_dict
from firefox_ua import USER_AGENT
from random import randint
from lxml import html
from flask import jsonify

logging.basicConfig(level=logging.INFO)


class Cdiscount_requests():
    
    def get_session(self, url, proxy=None):
        #self.sess = requests.Session()
        session = requests.session()
        session.verify = False
        session.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US;q=0.8,en;q=0.5',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Host': url.split('//')[-1].split('/')[0],
            'User-Agent' : USER_AGENT[randint(0, len(USER_AGENT)-1)]
        }
        if not proxy:
            return session

        proxies = {'http':proxy,'https':proxy}
        session.proxies=proxies
        return session
        
    def parse(self, url, proxy):
        session = self.get_session(url)
        splash_url = 'http://splash:8050/render.html'
        response = session.get(splash_url, params={'url': url, 'response_body': 1, 'cookies': True,
                                           'timeout': 10, 'wait': 5,  'js_enabled': True,
                                           'redirect': True, 'User-Agent' : USER_AGENT[randint(0, len(USER_AGENT)-1)]})
        try:
           tree = html.fromstring(response.content)
        except Exception as e:
            logging.info(f"Error tree {e}")
            return {'error':e}
        jsons = []
        for j in tree.xpath('//script[@type="application/ld+json"]/text()'):
            jsons.append(json.loads(j.strip()))
        return {"jsons": jsons, 'html': response.text}

