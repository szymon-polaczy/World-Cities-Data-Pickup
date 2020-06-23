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
            if ((city_data[i].find("Kod") != -1 and city_data[i+1].find("ISTAT") != -1) or
                (city_data[i].find("Kod") != -1 and city_data[i+1].find("ISO") != -1) or 
                (city_data[i].find("TERC") != -1 and city_data[i+1].find("TERYT") != -1) or 
                (city_data[i].find("Liczba") != -1 and city_data[i+1].find("rejonów") != -1) or
                (city_data[i].find("Liczba") != -1 and city_data[i+1].find("sielsowietów") != -1)):
                print("Connecting two places - KOD ISTAT / KOD ISO / TERC (TERYT) / Liczba rejonów / Liczba sielsowietów")
                city_data[i+1] = city_data[i] + city_data[i+1]
            elif (city_data[i].find("Urząd miejski") != -1 or city_data[i].find("Adres urzędu") != -1):
                print("Connecting two places - URZĄD MIEJSKI | ADRES URZĘDU")
                city_data[i+2] = city_data[i+1] + ' | ' + city_data[i+2]
                table.append(ele)
                del city_data[i+1]
            elif (ele.find("[") != -1 and ele.find("]") != -1 and city_data[i-1].find("Prawa miejskie") == -1): #ele == "Flaga" or ele == "flaga" or ele == "Herb" or ele == "herb" or ele.find("Plan") != -1 or ): #I THINK THIS IS NOT NEEDED _ MAYBE JUST THE []
                print("Deleted unused data")
            elif (ele.find("Położenie") != -1):
                break
            else:
                table.append(ele)
        i+=1

    #Additional Table Filtering
    table = list(filter(lambda x: x != '.', table))
    table = list(filter(lambda x: x != ',', table))
    table = list(filter(lambda x: x != '', table))

    #TRY_EXCEPT - Check if there is "Prawa miejskie" and what is after them
    try:
        inx = table.index("Prawa miejskie")

        if (table[inx + 2].isnumeric() == True):
            table[inx + 1] = table[inx + 1] + ' ' + table[inx + 2]
            del table[inx + 2]
    except ValueError:
        print("There was no - Prawa miejskie")

    #TRY_EXCEPT - Check if there is something extra between "Burmistrz" and "Powierzchnia"
    try:
        inx_b = table.index("Burmistrz")
        inx_p = table.index("Powierzchnia")

        if (inx_p - inx_b == 3):
            table[inx_b + 1] = table[inx_b + 1] + ' ' + table[inx_b + 2]
            del table[inx_b + 2]
    except ValueError:
        print("There was no - Burmistrz or Powierzchnia")

    #TRY_EXCEPT - Check if there is something extra between "Zarządzający" and "Powierzchnia"
    try:
        inx_b = table.index("Zarządzający")
        inx_p = table.index("Powierzchnia")

        if (inx_p - inx_b == 3):
            table[inx_b + 1] = table[inx_b + 1] + ' ' + table[inx_b + 2]
            del table[inx_b + 2]
    except ValueError:
        print("There was no - Zarządzający or Powierzchnia")

    #TRY_EXCEPT - Check if there is something extra between "Prawa miejskie" and "Burmistrz"
    try:
        inx_b = table.index("Prawa miejskie")
        inx_p = table.index("Burmistrz")

        if (inx_p - inx_b == 3): #NOT SURE WHY 4 AND NOT 3
            table[inx_b + 1] = table[inx_b + 1] + ' ' + table[inx_b + 2]
            del table[inx_b + 2]
    except ValueError:
        print("There was no - Prawa miejskie or Burmistrz")

    #TRY_EXCEPT - set correct position for "liczba ludności" and "gęstość"
    try:
        inx_b = table.index("liczba ludności")
        inx_p = table.index("gęstość")

        if (inx_p - inx_b == 1):
            tmp = table[inx_b + 1]
            table[inx_b + 1] = table[inx_b + 2]
            table[inx_b + 2] = tmp
    except ValueError:
        print("There was no - Liczba ludności or Gęstość")

    #TRY_EXCEPT - check if there is "Populacja" and corect date after
    try:
        inx = table.index("Populacja")

        if (table[inx + 1].find("liczba ludności") != -1 or table[inx + 1].find("gęstość") != -1):
            table.insert(inx + 1, "Brak daty")
        elif (table[inx + 2].isnumeric() == True):
            table[inx + 1] = table[inx + 1] + ' ' + table[inx + 2]
            del table[inx + 2]
    except ValueError:
        print("There was no - Populacja")

    #TRY_EXCEPT - check if there is "Symbole japońskie", if there is insert dummy data
    try:
        inx = table.index("Symbole japońskie")

        table.insert(inx + 1, " - ")
    except ValueError:
        print("There was no - Symbole japońskie")

    #TRY_EXCEPT - check if there is "Szczegółowy podział administracyjny", if there is insert dummy data
    try:
        inx = table.index("Szczegółowy podział administracyjny")

        table.insert(inx + 1, " - ")
    except ValueError:
        print("There was no - Szczegółowy podział administracyjny")

    #ANOTHER LOOP FOR END CLEANING
    i = 0
    for ele in table:
        table[i] = table[i].replace(']', '')
        table[i] = table[i].replace('[', '')
        table[i] = table[i].strip()

        try:
            if ((table[i - 1].find("km²") != -1 and table[i].find("km²") != -1) or table[i] == "km²" or table[i] == "m n.p.m." or (table[i].find("km²") != -1 and table[i-1].isnumeric() == True)):
                table[i - 1] = table[i - 1] + ' ' + table[i]
                del table[i]
            elif (table[i] == "potrzebny przypis"):
                del table[i]
        except Exception as ex:
            print(ex)

        i+=1

    #IMAGE DATA - I'm getting addititional image data for the city
    img_data = tree.xpath('//tr[@class="grafika-z-wikidanych"]/td/a/img/@src')

    if (img_data == []):
        img_data = tree.xpath('//table[@class="infobox"]/tbody/tr/td/a[@class="image"]/img/@src')

        if (img_data == []):
            img_data = None

    #GEO DATA - I'm getting just the geo data directly from the wiki table
    geo_data = tree.xpath('//table[@class="infobox"]/tbody/tr/td/span/a/span/span/descendant-or-self::text()')
    if (geo_data != []):
        geo_pres_data = {
            "latitude": geo_data[0],
            "longitude": geo_data[2]
        }

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
        ntable.insert(0, ['Img Source', img_data[0]])

    if (geo_data != []):
        ntable.insert(0, ["Geo Location", geo_pres_data])

    if (type_data != []):
        ntable.insert(0, ["Rodzaj Miejscowośći", type_data[1]])
    else:
        ntable.insert(0, ["Rodzaj Miejscowośći", "Brak Danych"])

    if (name_data != []):
        ntable.insert(0, ["Nazwa", name_data[0]])

    return ntable

print(city_data("/wiki/S%C5%82ubice"))