#!/usr/bin/python

'''
Scrape all python package url.
'''

__author__ = "Shahraan Hussain"

from multiprocessing import Process,Pipe
import requests
from lxml import html
import yaml
from datetime import datetime


class bot:
    def __init__(self):

        with open('./config.yml', 'r') as file:
            config = yaml.safe_load(file)
        if config:
            self.url = config['base_url']
            self.pagin_xpath = config['pagin_xpath']
            self.pack_xpath = config['pack_url_xpath']
            self.pip_xpath = config['pip_xpath']
            

    def pagin_url(self):
        response = requests.get(self.url)
        pagin = []
        template_url = "https://pypi.org/search/?c=Programming+Language+%3A%3A+Python+%3A%3A+3&page="
        if response.status_code == 200:
            dom = html.fromstring(response.content)
            last_page = dom.xpath(self.pagin_xpath)
            last_page_value = last_page[-1] if len(last_page)> 0 else print("Last page array is empty, Check pagin xapth")
            int_page = int(last_page_value)
            for page in range(1,int_page+1):
                page_url = template_url+str(page)
                pagin.append(page_url)
        
        return pagin[:10]
    
    def fetch_package_url(self,pagin_url):
        template_url = "https://pypi.org"
        fin_urls = []
        for url in pagin_url:
            response = requests.get(url)
            if response.status_code == 200:
                dom = html.fromstring(response.content)
                pack_url = dom.xpath(self.pack_xpath)
                for url in pack_url:
                    final_url = template_url+url
                    fin_urls.append(final_url)
                    

        return fin_urls
    
    def get_pip_command(self,pack_urls):
        pip_command_list = []
        for url in pack_urls:
            response = requests.get(url)
            if response.status_code == 200:
                dom = html.fromstring(response.content)
                pip_command = dom.xpath(self.pip_xpath)
                pip_command_list.append(pip_command[0])
                print(pip_command)
        return pip_command_list


        



if __name__ == "__main__":
    initial_time = datetime.now()
    scraper = bot()
    page_url = scraper.pagin_url()
    pack_url = scraper.fetch_package_url(page_url)
    final_command = scraper.get_pip_command(pack_url)
    final_time = datetime.now()
    time_difference = (final_time-initial_time).total_seconds()
    print(time_difference)
