from lxml import html
import requests

page = requests.get('https://pl.wikipedia.org/wiki/Adrano')
#page = requests.get('https://en.wikipedia.org/wiki/Nysa,_Poland')
tree = html.fromstring(page.content)

#ogtable = tree.xpath('//table[@class="infobox geography vcard"]/tbody/tr/td/descendant-or-self::text()')
ogtable = tree.xpath('//table[@class="infobox"]/tbody/tr/td/descendant-or-self::text()')

#for ele in ogtable:
 #   print(ele)

#print(ogtable)

i = 0
table = []
for ele in ogtable:
    ele = ele.replace("\n", '')
    ele = ele.replace("•", '')
    ele = ele.replace("\xa0", ' ')
    ele = ele.replace("/", '')
    ele = ele.replace("—", '')
    ele = ele.replace("(", '')
    ele = ele.replace(")", '')
    ele = ele.replace("\ufeff", '')
    ele = ele.strip()
    if (ele != '' and ele != ' '):
        table.append(ele)
    #table.append(ele)
    i+=1

print(table)
#
#for ele in table:
 #   ele = ele.replace('\n', ' ')
   # print(ele)

#print('Table', table)