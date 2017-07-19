from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import quote
import json
import time
def main():
    heroList = ['Abathur']
    heroJSON = {}
    with open('herolist.txt') as f:
          heroList = f.read().splitlines()
    for hero in heroList:
        page = 'https://www.hotslogs.com/Sitewide/HeroDetails?Hero=' + heroList[heroList.index(hero)]
        page = quote(page, safe="%/:=&?~#+!$,;'@()*[].")
        talentList = ""
        actualPage = urlopen(page)
        soup = BeautifulSoup(actualPage, 'html.parser')
        info = soup.find(id="ctl00_MainContent_RadGridPopularTalentBuilds_ctl00__0")
        try:
            tierList = [1,4,7,10,13,16]
            counter = 0
            info = info.find_all("td", align='center')
            #print("align=\"center\"")
            counter2 = 1
            for item in info:
                #print("Item #" + str(counter2) + " in item loop!")
                img = item.find('img', alt=True)
                try:
                    talentList = talentList + "Level " + str(tierList[counter]) + ": " + (img['alt'].split(':')[0] + ". ")
                except TypeError:
                    talentList = talentList + "Level " + str(tierList[counter]) + ": Player's Choice "
                #print("Current list: " + talentList)
                counter += 1
                counter2 += 1
                if (counter == 6):
                    break
        except AttributeError:
            talentList = "NoBuildsFound"
        heroJSON[hero] = talentList
        time.sleep(3)
        print("Finshed creating " + hero + "!")
    #for item in info:
     #   if 'style' in item:
      #      print (info['style'])
       #     print (info['style'] == 'display:none')
    #info = info.findChildren()
    #for child in info:
     #   if 'style' in child:
      #      print("style is :" + child['style'])
       #     #if child['style'] == 'display:none;':
                    #print(child)
        #else:
         #   print("This isnt working...")
        #print (child.select( '[style~="display:none"]' ))
    #print(info)
    print(heroJSON)
    with open('herobuilds.json','w') as outfile:
        json.dump(heroJSON, outfile)
    print("Done!")
    
main()
