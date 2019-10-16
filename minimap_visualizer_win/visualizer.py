import tkinter as tk
from tkinter.constants import *
import random
from PIL import ImageTk, Image, ImageDraw

class VisualizerCanvas(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, kwargs)

        self.master = master
        self.configure(width=self.master.winfo_width()-10, height=self.master.winfo_height()-10)
        self.game_data = None
        self.current_time = 0


        self.render_champions = True
        self.champion_color = (255, 0, 0)
        self.render_camps = True
        self.camp_color = "#00FF00"

        self.render_background = True

        self.minimap_size = 295 # width, height of input coordinates

        self.reference_size = self.winfo_width()

        self.champion_circle_circumference = int(self.reference_size/40)

        self.background_image_object = Image.open("res/actual-back.png")

        self.color_tags = ['AntiqueWhite1', 'AntiqueWhite2', 'AntiqueWhite3', 'AntiqueWhite4', 'CadetBlue1',
                           'CadetBlue2', 'CadetBlue3', 'CadetBlue4', 'DarkGoldenrod1', 'DarkGoldenrod2',
                           'DarkGoldenrod3', 'DarkGoldenrod4', 'DarkOliveGreen1', 'DarkOliveGreen2', 'DarkOliveGreen3',
                           'DarkOliveGreen4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4', 'DarkOrchid1',
                           'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4', 'DarkSeaGreen1', 'DarkSeaGreen2',
                           'DarkSeaGreen3', 'DarkSeaGreen4', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3',
                           'DarkSlateGray4', 'DeepPink2', 'DeepPink3', 'DeepPink4', 'DeepSkyBlue2', 'DeepSkyBlue3',
                           'DeepSkyBlue4', 'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'HotPink1', 'HotPink2',
                           'HotPink3', 'HotPink4', 'IndianRed1', 'IndianRed2', 'IndianRed3', 'IndianRed4',
                           'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'LemonChiffon2', 'LemonChiffon3',
                           'LemonChiffon4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4', 'LightCyan2',
                           'LightCyan3', 'LightCyan4', 'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3',
                           'LightGoldenrod4', 'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'LightSalmon2',
                           'LightSalmon3', 'LightSalmon4', 'LightSkyBlue1', 'LightSkyBlue2', 'LightSkyBlue3',
                           'LightSkyBlue4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3', 'LightSteelBlue4',
                           'LightYellow2', 'LightYellow3', 'LightYellow4', 'MediumOrchid1', 'MediumOrchid2',
                           'MediumOrchid3', 'MediumOrchid4', 'MediumPurple1', 'MediumPurple2', 'MediumPurple3',
                           'MediumPurple4', 'MistyRose2', 'MistyRose3', 'MistyRose4', 'NavajoWhite2', 'NavajoWhite3',
                           'NavajoWhite4', 'OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'OrangeRed2', 'OrangeRed3',
                           'OrangeRed4', 'PaleGreen1', 'PaleGreen2', 'PaleGreen3', 'PaleGreen4', 'PaleTurquoise1',
                           'PaleTurquoise2', 'PaleTurquoise3', 'PaleTurquoise4', 'PaleVioletRed1', 'PaleVioletRed2',
                           'PaleVioletRed3', 'PaleVioletRed4', 'PeachPuff2', 'PeachPuff3', 'PeachPuff4', 'RosyBrown1',
                           'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3',
                           'RoyalBlue4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'SkyBlue1', 'SkyBlue2', 'SkyBlue3',
                           'SkyBlue4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3', 'SlateBlue4', 'SlateGray1',
                           'SlateGray2', 'SlateGray3', 'SlateGray4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4',
                           'SteelBlue1', 'SteelBlue2', 'SteelBlue3', 'SteelBlue4', 'VioletRed1', 'VioletRed2',
                           'VioletRed3', 'VioletRed4', 'alice blue', 'antique white', 'aquamarine', 'aquamarine2',
                           'aquamarine4', 'azure', 'azure2', 'azure3', 'azure4', 'bisque', 'bisque2', 'bisque3',
                           'bisque4', 'blanched almond', 'blue', 'blue violet', 'blue2', 'blue4', 'brown1', 'brown2',
                           'brown3', 'brown4', 'burlywood1', 'burlywood2', 'burlywood3', 'burlywood4', 'cadet blue',
                           'chartreuse2', 'chartreuse3', 'chartreuse4', 'chocolate1', 'chocolate2', 'chocolate3',
                           'coral', 'coral1', 'coral2', 'coral3', 'coral4', 'cornflower blue', 'cornsilk2', 'cornsilk3',
                           'cornsilk4', 'cyan', 'cyan2', 'cyan3', 'cyan4', 'dark goldenrod', 'dark green', 'dark khaki',
                           'dark olive green', 'dark orange', 'dark orchid', 'dark salmon', 'dark sea green',
                           'dark slate blue', 'dark slate gray', 'dark turquoise', 'dark violet', 'deep pink',
                           'deep sky blue', 'dim gray', 'dodger blue', 'firebrick1', 'firebrick2', 'firebrick3',
                           'firebrick4', 'floral white', 'forest green', 'gainsboro', 'ghost white', 'gold', 'gold2',
                           'gold3', 'gold4', 'goldenrod', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4',
                           'gray', 'gray1', 'gray10', 'gray11', 'gray12', 'gray13', 'gray14', 'gray15', 'gray16',
                           'gray17', 'gray18', 'gray19', 'gray2', 'gray20', 'gray21', 'gray22', 'gray23', 'gray24',
                           'gray25', 'gray26', 'gray27', 'gray28', 'gray29', 'gray3', 'gray30', 'gray31', 'gray32',
                           'gray33', 'gray34', 'gray35', 'gray36', 'gray37', 'gray38', 'gray39', 'gray4', 'gray40',
                           'gray42', 'gray43', 'gray44', 'gray45', 'gray46', 'gray47', 'gray48', 'gray49', 'gray5',
                           'gray50', 'gray51', 'gray52', 'gray53', 'gray54', 'gray55', 'gray56', 'gray57', 'gray58',
                           'gray59', 'gray6', 'gray60', 'gray61', 'gray62', 'gray63', 'gray64', 'gray65', 'gray66',
                           'gray67', 'gray68', 'gray69', 'gray7', 'gray70', 'gray71', 'gray72', 'gray73', 'gray74',
                           'gray75', 'gray76', 'gray77', 'gray78', 'gray79', 'gray8', 'gray80', 'gray81', 'gray82',
                           'gray83', 'gray84', 'gray85', 'gray86', 'gray87', 'gray88', 'gray89', 'gray9', 'gray90',
                           'gray91', 'gray92', 'gray93', 'gray94', 'gray95', 'gray97', 'gray98', 'gray99',
                           'green yellow', 'green2', 'green3', 'green4', 'honeydew2', 'honeydew3', 'honeydew4',
                           'hot pink', 'indian red', 'ivory2', 'ivory3', 'ivory4', 'khaki', 'khaki1', 'khaki2',
                           'khaki3', 'khaki4', 'lavender', 'lavender blush', 'lawn green', 'lemon chiffon',
                           'light blue', 'light coral', 'light cyan', 'light goldenrod', 'light goldenrod yellow',
                           'light grey', 'light pink', 'light salmon', 'light sea green', 'light sky blue',
                           'light slate blue', 'light slate gray', 'light steel blue', 'light yellow', 'lime green',
                           'linen', 'magenta2', 'magenta3', 'magenta4', 'maroon', 'maroon1', 'maroon2', 'maroon3',
                           'maroon4', 'medium aquamarine', 'medium blue', 'medium orchid', 'medium purple',
                           'medium sea green', 'medium slate blue', 'medium spring green', 'medium turquoise',
                           'medium violet red', 'midnight blue', 'mint cream', 'misty rose', 'navajo white', 'navy',
                           'old lace', 'olive drab', 'orange', 'orange red', 'orange2', 'orange3', 'orange4', 'orchid1',
                           'orchid2', 'orchid3', 'orchid4', 'pale goldenrod', 'pale green', 'pale turquoise',
                           'pale violet red', 'papaya whip', 'peach puff', 'pink', 'pink1', 'pink2', 'pink3', 'pink4',
                           'plum1', 'plum2', 'plum3', 'plum4', 'powder blue', 'purple', 'purple1', 'purple2', 'purple3',
                           'purple4', 'red', 'red2', 'red3', 'red4', 'rosy brown', 'royal blue', 'saddle brown',
                           'salmon', 'salmon1', 'salmon2', 'salmon3', 'salmon4', 'sandy brown', 'sea green',
                           'seashell2', 'seashell3', 'seashell4', 'sienna1', 'sienna2', 'sienna3', 'sienna4',
                           'sky blue', 'slate blue', 'slate gray', 'snow', 'snow2', 'snow3', 'snow4', 'spring green',
                           'steel blue', 'tan1', 'tan2', 'tan4', 'thistle', 'thistle1', 'thistle2', 'thistle3',
                           'thistle4', 'tomato', 'tomato2', 'tomato3', 'tomato4', 'turquoise', 'turquoise1',
                           'turquoise2', 'turquoise3', 'turquoise4', 'violet red', 'wheat1', 'wheat2', 'wheat3',
                           'wheat4', 'white smoke', 'yellow', 'yellow green', 'yellow2', 'yellow3', 'yellow4']
        self.available_color_tags = self.color_tags
        self.champ_colors = {}

        self.jungle_bbox = {
                            "blue_blue_buff": [
                              84,
                              135,
                              106,
                              157
                            ],
                            "blue_toad": [
                              58,
                              129,
                              76,
                              150
                            ],
                            "blue_wolves": [
                              84,
                              158,
                              107,
                              186
                            ],
                            "blue_chickens": [
                              142,
                              182,
                              159,
                              203
                            ],
                            "blue_red_buff": [
                              152,
                              202,
                              172,
                              229
                            ],
                            "blue_krugs": [
                              163,
                              226,
                              183,
                              248
                            ],
                            "red_blue_buff": [
                              213,
                              150,
                              231,
                              178
                            ],
                            "red_toad": [
                              238,
                              160,
                              255,
                              184
                            ],
                            "red_wolves": [
                              210,
                              130,
                              228,
                              149
                            ],
                            "red_chickens": [
                              153,
                              109,
                              175,
                              132
                            ],
                            "red_red_buff": [
                              141,
                              82,
                              162,
                              106
                            ],
                            "red_krugs": [
                              130,
                              65,
                              152,
                              83
                            ],
                            "bot_side_scuttle": [
                              204,
                              185,
                              223,
                              207
                            ],
                            "top_side_scuttle": [
                              97,
                              105,
                              116,
                              131
                            ]
                          }

        self.master.bind("<Configure>", self.onResize)

    def initialize(self, game_json_ob):
        self.clear_canvas()
        self.game_data = game_json_ob
        self.available_color_tags = self.color_tags
        self.champ_colors = {}

    def clear_canvas(self):
        self.delete(ALL)

    def onResize(self, event):
        if self.master.winfo_width() < 10: return 0
        reference_size = min(self.master.winfo_width(), self.master.winfo_height())   # add some pad
        print("resizing to", reference_size)
        self.config(width=reference_size, height=reference_size)
        self.reference_size = reference_size
        self.champion_circle_radius = int(self.reference_size / 40)

    def draw_background_image(self):
        self.delete("background")
        cropped_background_image_object = self.background_image_object.resize((self.winfo_height(), self.winfo_width()), Image.ANTIALIAS)
        self.background_image_tk = ImageTk.PhotoImage(cropped_background_image_object)
        self.create_image((0,0), image=self.background_image_tk, anchor=NW, tags="background")
        #self.create_line((0,0, 400,400), width=5)

    def draw_grid(self):
        #self.delete("grid")
        swidth = self.winfo_width()
        sheight = self.winfo_height()
        grid_overlay = Image.new("RGBA", (sheight, swidth), (0,0,0,0))
        draw = ImageDraw.Draw(grid_overlay)
        grid_size = int(self.winfo_width()/self.minimap_size)
        for x in range(self.minimap_size):
            draw.line([(x*grid_size, 0), (x*grid_size, swidth)], fill=(0,0,0), width=1)
            draw.line([(0, x*grid_size), (sheight, x*grid_size)], fill=(0, 0, 0), width=1)

        self.create_image((0,0), image=ImageTk.PhotoImage(grid_overlay), anchor=NW, tags="grid")

    def render(self, timestamp):
        self.clear_canvas()
        json_data = self.game_data["keyframes"][str(timestamp)]
        if self.render_background:
            self.draw_background_image()

        if self.render_camps:
            if "camp_data" in json_data.keys():
                for camp_name, value in json_data["camp_data"].items():
                    if value:
                        self.create_rectangle(list(map(lambda x: int(x*self.reference_size/self.minimap_size), self.jungle_bbox[camp_name])), outline=self.camp_color)

        for champion_name, data in json_data["champ_data"].items():
            center_x = int(((int(data["left"])+int(data["right"]))/2)*self.reference_size/self.minimap_size)
            center_y = int(((int(data["top"])+int(data["bottom"]))/2)*self.reference_size/self.minimap_size)
            bbox = (center_x-self.champion_circle_radius, center_y-self.champion_circle_radius, center_x+self.champion_circle_radius, center_y+self.champion_circle_radius)
            try:
                color = self.champ_colors[champion_name]
            except:
                color = random.choice(self.available_color_tags)
                self.available_color_tags.remove(color)
                self.champ_colors[champion_name] = color
            self.create_oval(bbox, fill=color, tags="champions")



if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("600x600+10+10")
    v = VisualizerCanvas(root, None)
    root.after(100, v.draw_background_image)
    root.mainloop()