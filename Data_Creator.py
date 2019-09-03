import json
import urllib.request
from bs4 import BeautifulSoup
import argparse
from PIL import Image
import os
import secrets


class DD_gatherer:
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

class DataCreator:
    def __init__(self, save, amount, noise, overlap):
        self.save = save
        self.amount = amount
        self.noise = noise
        self.overlap = overlap

    def saving():
        path = "./Data/" 
        
    def base_creating(self):
        mini_path = "./LOL_image/minimap/"
        
        with Image.open(mini_path + "mini_outter.png") as outter:
            self.width, self.height = width, height = outter.size
            minimap = Image.new("RGBA",(width, height))
            with Image.open(mini_path + "mini_inner.png") as inner:
                self.Size = Size = 50
                Inner = inner.resize((width - Size, height - Size))
                minimap.paste(Inner, (45, 45), Inner)
                minimap.paste(outter, (0,0), outter)
                #Inner.show()
                #minimap.show()

        self.base = minimap
        minimap.save(r"./Data/test_base.png")

    def hero_creating(self):
        hero_path = "./LOL_image/character/"
        self.position = []
        self.base_creating()
        minimap = self.base

        hero_list = os.listdir(hero_path)
        for i in range(len(hero_list)):
            if hero_list[i] == ".DS_Store":
                hero_list.pop(i)
                break

        Num = 10
        hero_ran = []
        for i in range(Num): hero_ran.append(secrets.choice(hero_list))

        for hero in hero_ran:
            width, height = secrets.randbelow(self.width - self.Size), secrets.randbelow(self.height - self.Size)
            width, height = width + self.Size, height + self.Size
            self.position.append([hero[:-4], width, height])
            HERO = Image.open(hero_path + hero).resize((64, 64))
            minimap.paste(HERO, (width, height), HERO)

        self.hero = minimap
        minimap.save(r"./Data/test_hero.png")

    def noise_creating(self):
        hero_path = "./LOL_image/character/"
        self.hero_creating()
        minimap = self.hero

        

if __name__ == "__main__":
    Parser = argparse.ArgumentParser()
    Parser.add_argument('--save', required=True, help = "type of save form to save data - png or npm")
    Parser.add_argument('--amount', required=True ,type=int, help = "Gathering Img for creating data")
    Parser.add_argument('--noise', required=True ,type=int, help = "amount of noise at each png")
    Parser.add_argument('--overlap', required=True ,type=int, help = "percent of overlapped with character img")
    Parser.add_argument('--gathering', required=False, type=bool, help = "Gathering Img for creating data")

    args = Parser.parse_args()

    if args.gathering == "True":
        #For image update
        gatherer = DD_gatherer()
        gatherer.get_character_list()
        gatherer.get_minimap_base()
        gatherer.get_minimap_noise()

    creator = DataCreator(args.save, args.amount, args.noise, args.overlap)
    #creator.base_creating()
    #creator.hero_creating()
    creator.noise_creating()
