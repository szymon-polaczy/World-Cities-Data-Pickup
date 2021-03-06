# coding=utf-8

from lxml import html
from city_data import city_data
import json
import requests

#page = requests.get('https://pl.wikipedia.org/wiki/Miasta_we_W%C5%82oszech')
#page = requests.get('https://pl.wikipedia.org/wiki/Miasta_w_Holandii')
#page = requests.get('https://pl.wikipedia.org/wiki/Miasta_Aruby')# - skup się dzisiaj na tym
#page = requests.get('https://pl.wikipedia.org/wiki/Miasta_w_Japonii')
#page = requests.get('https://pl.wikipedia.org/wiki/Miasta_w_Jordanii') - DOESN'T WORK
#page = requests.get('https://pl.wikipedia.org/wiki/Miasta_na_Bia%C5%82orusi')
page = requests.get('https://pl.wikipedia.org/wiki/Miasta_w_Polsce')
tree = html.fromstring(page.content)

#HREFS FOR CITIES IN LISTS
#hrefs = tree.xpath('//div[@id="mw-content-text"]/div/ul/li/a//@href')

#HREFS FOR CITIES IN TABLES - LIKE "BIAŁORUŚ"
#hrefs = tree.xpath('//table[@class="wikitable sortable"]/tbody/tr/td/a//@href')
#hrefs = list(dict.fromkeys(hrefs)) #Removing recurring values

#HREFS FOR CITIES IN TABLES LIKE LISTS - LIKE "POLSKA"
hrefs = tree.xpath('//div[@id="mw-content-text"]/div/div/ul/li/a//@href')
hrefs = list(dict.fromkeys(hrefs)) #Removing recurring values

ntable = {}
for i in range(len(hrefs)):
    if (hrefs[i][0] != '/' or hrefs[i][2] == '/' or hrefs[i][len(hrefs[i]) - 4] == '.'):
        continue

    ntable[hrefs[i].encode("utf-8").decode("utf-8")] = {}

    c_data = city_data(hrefs[i])

    try:
        if(c_data != None):
            for ele in c_data:
                ntable[hrefs[i].encode("utf-8").decode("utf-8")][ele[0]] = ele[1]
        else:
            ntable[hrefs[i].encode("utf-8").decode("utf-8")]["Dane"] = "Brak"
    except Exception as ex:
        ntable[hrefs[i].encode("utf-8").decode("utf-8")]["Error"] = str(ex)

f = open('data.json', 'w', encoding='utf-8')
json.dump(ntable, f, ensure_ascii=False)
f.closed
