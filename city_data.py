# coding=utf-8

from lxml import html
from muf import clear_string
import requests

def get_basic_city_data(city_name):
    page = requests.get('https://pl.wikipedia.org/wiki/' + city_name)

    if (page.status_code != 200):
        return None

    tree = html.fromstring(page.content)
    page_data = tree.xpath('//table[@class="infobox"]/tbody/tr/td/descendant-or-self::text()')

    #image_data = tree.xpath('//tr[@class="grafika-z-wikidanych"]/td/a/img/@src')
    #print(image_data)

    if (page_data == []):
        return None
    else:
        return page_data

def get_image_city_data(city_name):
    page = requests.get('https://pl.wikipedia.org/wiki/' + city_name)

    if (page.status_code != 200):
        return None

    tree = html.fromstring(page.content)
    image_data = tree.xpath('//tr[@class="grafika-z-wikidanych"]/td/a/img/@src')

    if (image_data == []):
        return None
    else:
        return image_data


def city_data(city_name):
    city_name = city_name.replace(' ', '_')

    city_data = get_basic_city_data(city_name)
    if (city_data == None):
        city_data = get_basic_city_data(city_name + "_(miasto)")
    if (city_data == None):
        city_data = get_basic_city_data(city_name + "_(Włochy)") #_(Nazwa Państwa) - my guess
    if (city_data == None):
        return None

    #print(city_data)
        
    i = 0
    table = []
    for ele in city_data: #LOOP FOR CLEANING
        ele = clear_string(ele)

        if (ele != '' and ele != ' '):
            if (ele.find("′E") != -1 or ele.find("′N") != -1 or ele.find('°N') != -1 or ele.find('°E') != -1 or ele.find('″N') != -1 or ele.find('″E') != -1):
                print("Deleted unused coordinates")
            elif (city_data[i-1].find("Położenie ") != -1 or city_data[i-3].find("Położenie ") != -1):
                print("Deleted unused data")
            elif (ele.find("Położenie") != -1):
                print("Deleted unused data")
                table.append("Położenie")
            elif (city_data[i].find("Kod") != -1 and city_data[i+1].find("ISTAT") != -1):
                print("Connecting two places - KOD ISTAT")
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
            elif (ele.find("Multimedia") != -1 or ele.find("Strona internetowa") != -1 or ele.find("Informacje w Wikipodróżach") != -1):
                break
            else:
                table.append(ele)
        i+=1

    #ANOTHER LOOP FOR END CLEANING
    i = 0
    for ele in table:
        if (ele == "Położenie"):
            try:
                float(table[i+1].replace(',', '.'))
                print("Connecting two places - COORDINATES")
                table[i+1] = table[i+1] + "'N | " + table[i+2] + "'E"
                table[i+1] = table[i+1].replace(",", '°')
                del table[i+2]
            except ValueError:
                print("false alarm - coordinates")  
        elif (table[i].find("miasto") != -1 and table[i+1] == 'i' or table[i].find("miasto") != -1 and table[i+1] == 'w' ):
            print("Connecting two places - TYPE OF PLACE")
            table[i] = table[i] + ' ' + table[i+1] + ' ' + table[i+2]
            del table[i+1]
            del table[i+1]
        elif (table[i] == ','):
            del table[i]
        elif (table[i - 2].find("Burmistrz") != -1 and table[i].find("PD") != -1 or table[i -2].find("Burmistrz") != -1 and table[i].find("VVD") != -1 or table[i -2].find("Burmistrz") != -1 and table[i].find("2014") != -1): #removing unnecessary words by the mayor's name
            del table[i]
        elif (table[i] == "km²"):
            table[i-1] = table[i-1] + ' ' + table[i]
            del table[i]
        elif (table[i - 1].find("km²") != -1 and table[i].find("km²") != -1):
            table[i - 1] = table[i - 1] + ' ' + table[i]
            del table[i]
        
        i+=1

    #This loops exists because I need to delete the images titles from the array
    while(True):
        #print(table)
        if (table[1].find("Państwo") == -1 and table[1].find("miasto") == -1 and table[1].find("gmina") == -1):
            del table[1]
            print("deleted words")
        elif (table[1].find("gmina") != -1 and table[2].find("Państwo") == -1 or table[1].find("gmina") != -1 and table[2].find("Państwo") == -1):
            del table[2]
            print("deleted second words")
        else:
            break
    


    #ANOTHER BIG TRY
    if (table[1][0] == table[0][0] and table[1][1] == table[0][1]):
        del table[1]
    
    if (table[1].find("miasto") == -1 and table[1].find("gmina") == -1 and table[1].find("Państwo") == -1):
        del table[1]

    if (table[1].find("’") != -1):
        del table[1]
        
    if (table[1] == "Państwo" or table[1] == "Region"):
        table.insert(0, "Nazwa")

    #BIG TRY _ POPULACJA
    try:
        inx = table.index("Populacja")

        if (table[inx + 1].find("liczba ludności") != -1 or table[inx + 1].find("gęstość") != -1):
            table.insert(inx + 1, "Brak daty")
    except ValueError:
        print("There was no - Populacja")


    #IMAGE DATA
    img_data = get_image_city_data(city_name)
    if (img_data == None):
        img_data = get_image_city_data(city_name + "_(miasto)")
    if (img_data == None):
        img_data = get_image_city_data(city_name + "_(Włochy)") #_(Nazwa Państwa) - my guess

        

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

    if (img_data != [] and img_data != None):
        ntable.insert(len(ntable)-1, ['IMG_SRC', img_data[0]])

    return ntable

#print(city_data("Dzierżyńska_Góra"))