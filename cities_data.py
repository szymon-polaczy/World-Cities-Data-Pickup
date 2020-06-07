# coding=utf-8

from lxml import html
from muf import clear_string
from city_data import city_data
import json
import requests
import copy

#page = requests.get('https://pl.wikipedia.org/wiki/Miasta_we_W%C5%82oszech')
#page = requests.get('https://pl.wikipedia.org/wiki/Miasta_w_Holandii')
#page = requests.get('https://pl.wikipedia.org/wiki/Miasta_na_Bia%C5%82orusi')
#page = requests.get('https://pl.wikipedia.org/wiki/Miasta_Aruby')
page = requests.get('https://pl.wikipedia.org/wiki/Miasta_w_Japonii')
tree = html.fromstring(page.content)

ogtable = tree.xpath('//div[@id="mw-content-text"]/div/ul/li/a/descendant-or-self::text()')
hrefs = tree.xpath('//div[@id="mw-content-text"]/div/ul/li/a//@href')

i = 0
for ele in ogtable: #LOOP FOR CLEANING

    if (i + 1 < len(ogtable)):
        if (ogtable[i].find("(") != -1):
            del ogtable[i]
    i+=1

i = 0
table = []
for ele in ogtable: #LOOP FOR CLEANING
    ele = clear_string(ele)

    if (ele != '' and ele != ' '):
        if (ele.find("City Population") != -1):
            break
        else:
            table.append(ele)
    i+=1

i = 0
ntable = {}
for ele in table:
    zw = table[i]

    #BANNED CITIES BECAUSE OF NAMES
    if (zw == "Boskoop" or zw == "Mutsu"):
        continue

    ntable[zw.encode("utf-8").decode("utf-8")] = {}


    c_data = city_data(hrefs[i])

    try:
        if(c_data != None):
            for ele in c_data:
                ntable[zw.encode("utf-8").decode("utf-8")][ele[0]] = ele[1]
        else:
            ntable[zw.encode("utf-8").decode("utf-8")]["Dane"] = "Brak"

    except Exception as ex:
        print("City - " + zw + " has this exception - " + str(ex))
        ntable[zw.encode("utf-8").decode("utf-8")]["Error"] = str(ex)

    i+=1

f = open('data.json', 'w', encoding='utf-8')
json.dump(ntable, f, ensure_ascii=False)
f.closed
