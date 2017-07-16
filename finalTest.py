from bs4 import BeautifulSoup
from urllib.request import urlopen
def main():
    heroRequest = 'Samuro'
    page = 'https://www.hotslogs.com/Sitewide/HeroDetails?Hero=' + heroRequest
    actualPage = urlopen(page)
    soup = BeautifulSoup(actualPage, 'html.parser')
    info = soup.find(id="ctl00_MainContent_RadGridPopularTalentBuilds_ctl00__0")
    info = info.find_all("td", style="display:none;")
    info = soup.find(id="ctl00_MainContent_RadGridPopularTalentBuilds_ctl00__0")
    info = info.find_all("td", style="display:none;")
    tiers = [1,4,7,10,13,16,20]
    i = 0
    speech_output = ""
    for item in info:
        currentTalent = item.text.strip()
        if(currentTalent):
            speech_output += "Level " + str(tiers[i]) + ": " + currentTalent + " "
            print("speech_output is " + speech_output)
            i += 1
    print("Done!")
    
main()
