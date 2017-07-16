from bs4 import BeautifulSoup
from urllib.request import urlopen
def main():
    heroRequest = 'Rexxar'
    page = 'https://www.hotslogs.com/Sitewide/HeroDetails?Hero=' + heroRequest
    actualPage = urlopen(page)
    soup = BeautifulSoup(actualPage, 'html.parser')
    info = soup.find(id="ctl00_MainContent_RadGridPopularTalentBuilds_ctl00__0")
    info = info.find_all("td", style="display:none;")
    for item in info:
        print(item.text.strip() + " ")
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
    print(info)
    print("Done!")
    
main()
