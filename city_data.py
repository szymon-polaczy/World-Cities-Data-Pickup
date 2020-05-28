# -*- coding: utf-8 -*-
from lxml import html
import requests

#page = requests.get('https://pl.wikipedia.org/wiki/Adrano')
#page = requests.get('https://pl.wikipedia.org/wiki/Nysa')
#page = requests.get('https://pl.wikipedia.org/wiki/Aci_Catena')
#page = requests.get('https://pl.wikipedia.org/wiki/Nowa_S%C3%B3l')
#page = requests.get('')
#page = requests.get('https://pl.wikipedia.org/wiki/Aprilia_(Latina)')
#page = requests.get('https://pl.wikipedia.org/wiki/Busto_Arsizio')
#page = requests.get('https://pl.wikipedia.org/wiki/Cesena')
#page = requests.get('https://pl.wikipedia.org/wiki/Conegliano')
page = requests.get('https://pl.wikipedia.org/wiki/Nak%C5%82o_nad_Noteci%C4%85')
tree = html.fromstring(page.content)

ogtable = tree.xpath('//table[@class="infobox"]/tbody/tr/td/descendant-or-self::text()')


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
        if (ele.find("′E") != -1 or ele.find("′N") != -1 or ele.find('°N') != -1 or ele.find('°E') != -1 or ele.find('″N') != -1 or ele.find('″E') != -1):
            print("Deleted unused coordinates")
        elif (ogtable[i-1].find("Położenie") != -1 or ogtable[i-3].find("Położenie") != -1):
            print("Deleted unused data")
        elif (ele.find("Położenie") != -1):
            print("Deleted unused data")
            table.append("Położenie")
        elif (ogtable[i].find("Kod") != -1 and ogtable[i+1].find("ISTAT") != -1):
            print("Connecting two places - KOD ISTAT")
            ogtable[i+1] = "Kod " + ogtable[i+1]
        elif (ogtable[i].find("TERC") != -1 and ogtable[i+2].find("TERYT") != -1):
            print("Connecting two places - TERC (TERYT)")
            ogtable[i+2] = "TERC | " + ogtable[i+2]
        elif (ogtable[i].find("Urząd miejski") != -1):
            print("Connecting two places - URZĄD MIEJSKI")
            ogtable[i+2] = ogtable[i+1] + ' | ' + ogtable[i+2]
            table.append(ele)
            del ogtable[i+1]
        elif (ele.find("[") != -1 and ele.find("]") != -1):
            print("Deleted unused data")
        elif (ele.find("Flaga") != -1 or ele.find("Herb") != -1):
            print("Deleted unused data")
        elif (ele.find("Multimedia") != -1):
            break
        else:
            table.append(ele)
    i+=1

#ANOTHER LOOP FOR END CLEANING
i = 0
for ele in table:
    if (ele == "Położenie"):
        print("Connecting two places - COORDINATES")
        table[i+1] = table[i+1] + "'N | " + table[i+2] + "'E"
        table[i+1] = table[i+1].replace(",", '°')
        del table[i+2]
    elif (table[i].find("miasto") != -1 and table[i+1] == 'i' or table[i].find("miasto") != -1 and table[i+1] == 'w' ):
        print("Connecting two places - TYPE OF PLACE")
        table[i] = table[i] + ' ' + table[i+1] + ' ' + table[i+2]
        del table[i+1]
        del table[i+1]
    elif (table[i] == ','):
        del table[i]
    elif (table[i-1].find("miasto") != -1):
        while (table[i].find("Państwo") == -1):
            del table[i]
    i+=1


#loop for new table
ntable = []
j = 0
k = -1
for ele in table:
    if (j % 2 == 0):
        ntable.append([])
        k+=1

    ntable[k].append(ele)
    j+=1
        

#print(table)
#print("\n\n\n")

for ele in ntable:
    print(ele)

#print(ntable)