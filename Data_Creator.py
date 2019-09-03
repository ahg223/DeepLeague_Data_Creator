import json
import urllib.request
from bs4 import BeautifulSoup
import argparse

class DD_gatherer():
    def __init__(self):
        self.opener=urllib.request.build_opener()
        self.opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(self.opener)
        self.latest_url='http://raw.communitydragon.org/latest/'
        self.local='./LOL_image/'


    def gathering(self, url, local):
        urllib.request.urlretrieve(url,local)

    def get_character_list(self):
        url = self.latest_url + "game/assets/characters/"
        version = input("typing version of LoL: ")
        Data = json.load(urllib.request.urlopen("http://ddragon.leagueoflegends.com/cdn/" + version + "/data/ko_KR/champion.json"))
        data = Data["data"]
        characters = list(data.keys())
        for i in range(len(characters)): characters[i] = characters[i].lower()

        with urllib.request.urlopen(url) as page:
            soup = BeautifulSoup(page.read(),"html.parser")
            page = soup.find("div", class_ = "card p-3")

            for link in page.find_all("a"):
                name = link.get("href")[:-1]
                if "tft" in name or name not in characters : continue
                
                page_url = url + name + "/hud" + "/"
                try: c_page = urllib.request.urlopen(page_url)
                except: continue

                c_soup = BeautifulSoup(c_page.read(),"html.parser")
                c_page = c_soup.find("div", class_ = "card p-3")
                for c_image in c_page.find_all("a"):
                    c_name = c_image.get("href")
                    if "circle" not in c_name: continue
                    else:
                        character_url = url + name + "/hud" + "/" + c_name
                        print(character_url)
                        self.gathering(character_url, self.local + "/character/" + c_name.split("_")[0] + ".png")
                        break


    def get_minimap_base(self):
        local = self.local + "minimap/"
        url = self.latest_url + "game/levels/map11/info/2dlevelminimap.png"
        self.gathering(url, local + "mini_inner.png")
        url = self.latest_url + "game/data/menu_sc4/minimapreplay_if.png"
        self.gathering(url, local + "mini_outter.png")
        
    def get_minimap_noise(self):
        local = self.local + "noise/"
        url = self.latest_url + "game/data/menu/minimapicons/"

        with urllib.request.urlopen(url) as page:
            soup = BeautifulSoup(page.read(),"html.parser")
            page = soup.find("div", class_ = "card p-3")

            for link in page.find_all("a"):
                name = link.get("href")
                Test_icon = ["bard", "palisades", "leblanc", "odyssey", "victimcounter", "yorick", "test", "tt"]
                if ".png" not in name: continue
                Flag = False
                for error in Test_icon:
                    if error in name:
                        Flag = True
                        break
                    
                if Flag: continue
                print(url+name)
                try: self.gathering(url+name, local+name)
                except: continue

class DataCreator():
    def init(self, ):

if __name == "__main__":
    parser = argparse.ArgumentParser()
    Parser.add_argument('--gathering', required=False, type=bool, help = "Gathering Img for creating data")
    Parser.add_argument('--save', required=True, help = "type of save form to save data - png or npm")
    Parser.add_argument('--amount', required=True ,type=int, help = "Gathering Img for creating data")
    Parser.add_argument('--noise', required=True ,type=int, help = "amount of noise at each png")
    Parser.add_argument('--overlap', required=True ,type=int, help = "percent of overlapped with character img")

    if args.gathering == "True":
        #For image update
        gatherer = DD_gatherer()
        gatherer.get_character_list()
        gatherer.get_minimap_base()
        gatherer.get_minimap_noise()


