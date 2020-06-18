# coding=utf-8

from lxml import html
from muf import clear_string
import requests    

def city_data(city_name):
    print(city_name)
    page = requests.get('https://pl.wikipedia.org' + city_name)

    if (page.status_code != 200):
        return None

    tree = html.fromstring(page.content)
    city_data = tree.xpath('//table[@class="infobox"]/tbody/tr/td/descendant-or-self::text()')

    if (city_data == []):
        return None
        
    i = 0
    table = []
    bylo_panstwo = False
    for ele in city_data: #LOOP FOR CLEANING
        ele = clear_string(ele)

        if (ele != '' and ele != ' ' and (ele.find("Państwo") != -1 or bylo_panstwo == True)):
            bylo_panstwo = True
            if (city_data[i].find("Kod") != -1 and city_data[i+1].find("ISTAT") != -1):
                print("Connecting two places - KOD ISTAT")
                city_data[i+1] = "Kod " + city_data[i+1]
            elif (city_data[i].find("Kod") != -1 and city_data[i+1].find("ISO") != -1):
                print("Connecting two places - KOD ISO")
                city_data[i+1] = "Kod " + city_data[i+1]
            elif (city_data[i].find("TERC") != -1 and city_data[i+2].find("TERYT") != -1):
                print("Connecting two places - TERC (TERYT)")
                city_data[i+2] = "TERC | " + city_data[i+2]
            elif (city_data[i].find("Urząd miejski") != -1 or city_data[i].find("Adres urzędu") != -1):
                print("Connecting two places - URZĄD MIEJSKI | ADRES URZĘDU")
                city_data[i+2] = city_data[i+1] + ' | ' + city_data[i+2]
                table.append(ele)
                del city_data[i+1]
            elif (ele.find("[") != -1 and ele.find("]") != -1):
                print("Deleted unused data")
            elif (ele.find("Flaga") != -1 or ele.find("Herb") != -1 or ele.find("flaga") != -1 or ele.find("herb") != -1):
                print("Deleted unused data")
            elif (ele.find("Plan") != -1):
                print("Deleted unused data")
            elif (ele.find("Położenie") != -1):
                break
            else:
                table.append(ele)
        i+=1

    #ANOTHER LOOP FOR END CLEANING
    i = 0
    for ele in table:
        table[i] = table[i].replace(']', '')
        table[i] = table[i].replace('[', '')
        table[i] = table[i].strip()

        try:
            if (table[i] == ','):
                del table[i]
            elif (table[i - 2].find("Burmistrz") != -1 and table[i].find("PD") != -1 or table[i -2].find("Burmistrz") != -1 and table[i].find("VVD") != -1 or table[i -2].find("Burmistrz") != -1 and table[i].find("2014") != -1): #removing unnecessary words by the mayor's name
                del table[i]
            elif (table[i] == "km²"):
                table[i-1] = table[i-1] + ' ' + table[i]
                del table[i]
            elif (table[i - 1].find("km²") != -1 and table[i].find("km²") != -1):
                table[i - 1] = table[i - 1] + ' ' + table[i]
                del table[i]
            elif (table[i] == "potrzebny przypis" or table[i] == ''):
                del table[i]
        except Exception as ex:
            print(ex)

        i+=1

    #TRY_EXCEPT - I'm using it to check if there even is "Populacja" and decide what to do next after checking if there is a date after it
    try:
        inx = table.index("Populacja")

        if (table[inx + 1].find("liczba ludności") != -1 or table[inx + 1].find("gęstość") != -1):
            table.insert(inx + 1, "Brak daty")
    except ValueError:
        print("There was no - Populacja")

    #TRY_EXCEPT - I'm using it to check if there even is "Symbole japońskie" and decide what to do next after checking if there is a date after it
    try:
        inx = table.index("Symbole japońskie")

        table.insert(inx + 1, " - ")
    except ValueError:
        print("There was no - Symbole japońskie")

    #IMAGE DATA - I'm getting addititional image data for the city
    img_data = tree.xpath('//tr[@class="grafika-z-wikidanych"]/td/a/img/@src')

    if (img_data == []):
        img_data = tree.xpath('//table[@class="infobox"]/tbody/tr/td/a[@class="image"]/img/@src')

        if (img_data == []):
            img_data = None

    #GEO DATA - I'm getting just the geo data directly from the wiki table
    geo_data = tree.xpath('//table[@class="infobox"]/tbody/tr/td/span/a/span/span/descendant-or-self::text()')
    if (geo_data != []):
        geo_pres_data = geo_data[0] + ' | ' + geo_data[2]

    #NAME & TYPE OF THE CITY DATA - I'm trying to get the full name of the city and the type of it
    name_data = tree.xpath('//table[@class="infobox"]/tbody/tr/td/table/tbody/tr/td/span/descendant-or-self::text()')
    type_data = tree.xpath('//table[@class="infobox"]/tbody/tr/td/table[@class="void"]/tbody/tr/td/descendant-or-self::text()')

    #loop for new table
    ntable = []
    k = -1
    for i in range(len(table)):
        if (i % 2 == 0):
            ntable.append([])
            k+=1

        ntable[k].append(table[i])

    if (img_data != [] and img_data != None):
        ntable.insert(0, ['IMG_SRC', img_data[0]])

    if (geo_data != []):
        ntable.insert(0, ["GEO_LOCATION", geo_pres_data])

    if (type_data != []):
        ntable.insert(0, ["RODZAJ MIEJSCOWOŚCI", type_data[1]])
    else:
        ntable.insert(0, ["RODZAJ MIEJSCOWOŚCI", "Brak Danych"])

    if (name_data != []):
        ntable.insert(0, ["NAZWA", name_data[0]])

    return ntable