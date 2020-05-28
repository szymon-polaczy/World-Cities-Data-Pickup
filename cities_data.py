#!/usr/bin/env python
# coding=utf-8

from lxml import html
import json
import requests
import copy

page = requests.get('https://pl.wikipedia.org/wiki/Miasta_we_W%C5%82oszech')
tree = html.fromstring(page.content)

ogtable = tree.xpath('//div[@id="mw-content-text"]/div/ul/li/descendant-or-self::text()')

i = 0
for ele in ogtable: #LOOP FOR CLEANING
    if (i + 1 < len(ogtable)):
        if (ogtable[i].find("(") != -1):
            del ogtable[i]
    i+=1

i = 0
table = []
for ele in ogtable: #LOOP FOR CLEANING
    ele = ele.replace("\n", '')
    ele = ele.replace("•", '')
    ele = ele.replace("\xa0", ' ')
    ele = ele.replace("/", '')
    ele = ele.replace("—", '')
    ele = ele.replace("(", '')
    ele = ele.replace(")", '')
    ele = ele.replace(":", '')
    ele = ele.replace("\ufeff", '')
    ele = ele.strip()
    if (ele != '' and ele != ' '):
        if (ele.find("City Population") != -1):
            break
        else:
            table.append(ele)
    i+=1

#print(table)

i = 0
ntable = {}
for ele in table:
    zw = table[i]
    ntable[zw.encode("utf-8").decode("utf-8")] = {}
    #ntable[i][zw] = {}
    i+=1

f = open('data.json', 'w', encoding='utf-8')
json.dump(ntable, f, ensure_ascii=False)
#json_string = json.dumps(ntable, ensure_ascii=False)

#f = json.dumps(json_string, f)

f.closed

#TRZEBA ZAMIENIĆ WSZYSTKIE SPACJE NA _ ŻEBY DOBRZE LINKI DZIAŁAŁY

# BĘDZIE ŹLE DZIAŁAĆ JEŚLI MASZ POWIEDZMY NA STRONIE WŁOSKIEJ - Orio al Serio - I tylko Serio to link - przez co orio al i serio są osobno liczone i żadne nie ma linku
# mógłbym spróbować coś napisać że sprawdza czy w połączeniu z następnym elementem ma dobrze ale to na przyszłość

#print(requests.get('https://pl.wikipedia.org/wiki/Abano_Terme'))
i =0
for ele in ntable:
    ele = ele.replace(' ', '_')
    page = requests.get('https://pl.wikipedia.org/wiki/' + ele)
    print(ele + '    ' + str(page))
    i+=1

print(i)