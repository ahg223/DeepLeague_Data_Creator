import json
import urllib.request
from bs4 import BeautifulSoup
import argparse
from PIL import Image
import os
import secrets
from copy import deepcopy
import numpy as np

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
        url = self.latest_url + "game/data/menu/textures/spectatorupdate.png"
        self.gathering(url, local + "mini_outter.png")

    def get_minimap_noise(self):
        local = self.local + "noise/"
        local_big = self.local + "ping/"
        url = self.latest_url + "game/data/menu/minimapicons/"

        with urllib.request.urlopen(url) as page:
            soup = BeautifulSoup(page.read(),"html.parser")
            page = soup.find("div", class_ = "card p-3")

            for link in page.find_all("a"):
                name = link.get("href")
                Test_icon = ["bard", "palisades", "odyssey", "victimcounter", "yorick", "test", "tt", "as", "center", "cool", "cry", "dark", "destroy", "doom", "enemyp", "energy", "neutral", "friendly", "health", "king", "cp", "quest", "sg", "cannon", "slime", "sre", "vilemaw", "vo"]
                if ".png" not in name: continue
                Flag = False
                for error in Test_icon:
                    if error in name:
                        Flag = True
                        break
                    
                if Flag: continue
                print(url+name)

                Flag = True
                big = ["ring", "tele", "recall", "tunnel"]
                for arg in big:
                    if arg in name:
                        try: self.gathering(url+name, local_big+name)
                        except: continue
                        Flag = False
                        break

                if Flag:
                    try: self.gathering(url+name, local+name)
                    except: continue

class DataCreator:
    def __init__(self, save, amount, noise, overlap, ping):
        self.save = save
        self.amount = amount
        self.noise_len = noise
        self.overlap = overlap
        self.ping_len = ping
        self.DATA = []

    def stack(self):
        if self.save == "png": self.DATA.append(deepcopy(self.ping))
        elif self.save == "npy": self.DATA.append(np.array(self.ping))

    def saving(self):
        if self.save == "png":
            count = 0
            for img in self.DATA:
                img.save("./Data/"+ str(count) + ".png")
                count += 1
                
        elif self.save == "npy": np.save("./Data/Numpy.npy",self.DATA)
        
        
    def base_creating(self):
        mini_path = "./LOL_image/minimap/"
        
        with Image.open(mini_path + "mini_outter.png") as outter:
            self.width, self.height = width, height = outter.size
            minimap = Image.new("RGBA",(width, height))
            with Image.open(mini_path + "mini_inner.png") as inner:
                self.Size = Size = 215
                self.innerwidth, self.innerheight = width - Size -15, height - Size -15
                Inner = inner.resize((self.innerwidth, self.innerheight))
                minimap.paste(Inner, (Size, Size), Inner)
                minimap.paste(outter, (0,0), outter)
                #Inner.show()
                #minimap.show()

        self.base = minimap
        minimap.save(r"./Data/test_base.png")

    def hero_creating(self):
        hero_path = "./LOL_image/character/"
        noise_path = "./LOL_image/noise/"
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

        count = 0
        for hero in hero_ran:
            count+=1
            if count > 5: Base = Image.open(noise_path + "leblanc_fake_allyteam.png").resize((34, 34))
            else: Base = Image.open(noise_path + "leblanc_fake_enemyteam.png").resize((34, 34))
            width, height = secrets.randbelow(self.innerwidth), secrets.randbelow( self.innerheight)
            width, height = width + self.Size, height + self.Size
            self.position.append([hero[:-4], width, height])
            HERO = Image.open(hero_path + hero).resize((30, 30))
            minimap.paste(Base, (width-2, height-2), Base)
            minimap.paste(HERO, (width, height), HERO)

        self.hero = minimap
        minimap.save(r"./Data/test_hero.png")

    def noise_creating(self):
        noise_path = "./LOL_image/noise/"
        self.hero_creating()
        minimap = self.hero
        noise_list = os.listdir(noise_path)

        for i in range(len(noise_list)):
            if noise_list[i] == ".DS_Store":
                noise_list.pop(i)
                break

        noise_ran = []
        for i in range(self.noise_len): noise_ran.append(secrets.choice(noise_list))
        print(noise_ran)

        for noise in noise_ran:
            width, height = secrets.randbelow(self.innerwidth), secrets.randbelow( self.innerheight)
            width, height = width + self.Size, height + self.Size
            NOISE = Image.open(noise_path + noise)
            if NOISE.size[1] > 16: NOISE.resize((16, 16))
            minimap.paste(NOISE, (width, height), NOISE)

        self.noise = minimap
        minimap.save(r"./Data/test_noise.png")

    def ping_creating(self):
        ping_path = "./LOL_image/ping/" 
        self.noise_creating()
        minimap = self.noise
        ping_list = os.listdir(ping_path)

        for i in range(len(ping_list)):
            if ping_list[i] == ".DS_Store":
                ping_list.pop(i)
                break

        ping_ran = []
        for i in range(self.ping_len): ping_ran.append(secrets.choice(ping_list))
        print(ping_ran)

        for ping in ping_ran:
            width, height = secrets.randbelow(self.innerwidth), secrets.randbelow(self.innerheight)
            width, height = width + self.Size, height + self.Size
            PING = Image.open(ping_path + ping).resize((34, 34))
            #if PING.size[1] > 32: PING.resize((34, 34))
            minimap.paste(PING, (width, height), PING)

        self.ping = minimap
        #minimap.show()
        minimap.save(r"./Data/test_ping.png")
        


if __name__ == "__main__":
    Parser = argparse.ArgumentParser()
    Parser.add_argument('--save', required=True, help = "type of save form to save data - png or npm")
    Parser.add_argument('--amount', required=True ,type=int, help = "Gathering Img for creating data")
    Parser.add_argument('--noise', required=True ,type=int, help = "amount of noise at each png")
    Parser.add_argument('--overlap', required=True ,type=int, help = "percent of overlapped with character img")
    Parser.add_argument('--ping', required=True ,type=int, help = "amount of ping at each png")
    Parser.add_argument('--gathering', required=False, type=bool, help = "Gathering Img for creating data")

    args = Parser.parse_args()

    if args.gathering:
        #For image update
        gatherer = DD_gatherer()
        gatherer.get_character_list()
        gatherer.get_minimap_base()
        gatherer.get_minimap_noise()

    creator = DataCreator(args.save, args.amount, args.noise, args.overlap, args.ping)
    #creator.base_creating()
    #creator.hero_creating()
    #creator.noise_creating()

    for _ in range(args.amount):
        creator.ping_creating()
        creator.stack()
        
    creator.saving()

    
    
