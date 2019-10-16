import tkinter as tk
import os
import json
from tkinter.constants import *
from tkinter.filedialog import askopenfilename
from tkinter.colorchooser import askcolor
from tkinter.ttk import Treeview, Combobox

class ControllerOptionMenu(tk.Frame):
    def __init__(self, master, visualizer_canvas, data_viewer,  **kwargs):
        super().__init__(master, kwargs)
        self.master = master
        self.visualizer = visualizer_canvas

        self.data_file_path = tk.StringVar()
        self.data_json_obj = None
        self.data_duration = tk.IntVar()

        self.data_viewer = data_viewer
        self.data_viewer.recreate_headers()

        self.render_champions_option = tk.BooleanVar()
        self.render_champions_color = tk.StringVar()
        self.render_champions_color.set("#FF0000")
        self.render_camps_option = tk.BooleanVar()
        self.render_camps_color = tk.StringVar()
        self.render_camps_color.set("#E1C699")

        self.playback_speed = tk.StringVar()
        self.playback_speed.set("1")
        self.playback_frames = tk.IntVar()
        self.playback_frames.set(1)
        self.playback_current_time = tk.IntVar()
        self.playback_state = tk.BooleanVar()
        self.playback_state.set(False)

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

    def draw_widgets(self):
        self.clear_widgets()

        option_frame = tk.Frame(self)
        option_frame.pack(expand=YES, fill=X, anchor=N)

        metadata_frame = tk.LabelFrame(option_frame, text="기본", relief=RAISED)
        metadata_frame.pack(side=TOP, expand=YES, fill=BOTH)
        metadata_frame.columnconfigure(0, weight=1)
        metadata_frame.columnconfigure(1, weight=1)
        self.path_label = tk.Label(metadata_frame, text="선택된 파일 없음", width=50, relief=RAISED, borderwidth=0)
        self.path_label.grid(row=0, column=0)

        tk.Button(metadata_frame, text="데이터파일 선택", command=self.onFileSelect).grid(row=0, column=1)

        tk.Label(metadata_frame, text="길이", borderwidth=1, relief=SOLID).grid(row=1, column=0, sticky=N+S+E+W, padx=(5, 0), pady=1)
        tk.Label(metadata_frame, textvariable=self.data_duration, borderwidth=1, relief=SOLID).grid(row=1, column=1, sticky=N+S+E+W, padx=(0, 5), pady=1)

        #tk.Label(metadata_frame, text="display_time", borderwidth=1, relief=SOLID).grid(row=2, column=0, sticky=N + S + E + W,padx=(5, 0), pady=1)
        #tk.Label(metadata_frame, textvariable=self.data_current_time, borderwidth=1, relief=SOLID).grid(row=2, column=1, sticky=N + S + E + W, padx=(0, 5), pady=1)


        render_options_frame = tk.LabelFrame(option_frame, text="그리기설정", relief=RAISED)
        render_options_frame.pack(side=TOP, expand=YES, fill=BOTH)
        render_options_frame.columnconfigure(0, weight=1)

        tk.Label(render_options_frame, text="챔피언", borderwidth=0).grid(row=0, column=0, sticky=N+S+E+W)
        tk.Checkbutton(render_options_frame, variable=self.render_champions_option, borderwidth=0).grid(row=0, column=1)
        tk.Button(render_options_frame, bg=self.render_champions_color.get(), width=2, borderwidth=0, command=lambda: self.set_color(self.render_champions_color)).grid(row=0, column=2, padx=(0,4), pady=(0,4))

        tk.Label(render_options_frame, text="정글", borderwidth=0).grid(row=1, column=0, sticky=N + S + E + W)
        tk.Checkbutton(render_options_frame, variable=self.render_camps_option, borderwidth=0).grid(row=1, column=1)
        tk.Button(render_options_frame, bg=self.render_camps_color.get(), width=2, borderwidth=0, command=lambda: self.set_color(self.render_camps_color)).grid(row=1, column=2, padx=(0, 4), pady=(0, 4))


        navigation_frame = tk.LabelFrame(option_frame, text="제어", relief=RAISED)
        navigation_frame.pack(side=TOP, expand=YES, fill=BOTH)
        navigation_frame.columnconfigure(0, weight=1)
        navigation_frame.columnconfigure(1, weight=1)

        tk.Label(navigation_frame, text="재생 속도", borderwidth=0).grid(row=0, column=0, sticky=N + S + E + W,pady=4)
        #tk.Entry(navigation_frame, textvariable=self.playback_speed, width=3, borderwidth=0).grid(row=0, column=1)
        speed_selector_combobox = Combobox(navigation_frame, textvariable=self.playback_speed, values=("1", "2", "4", "8"))
        speed_selector_combobox.current(0)
        speed_selector_combobox.grid(row=0, column=1, pady=4)

        tk.Label(navigation_frame, text="재싱 프레임 수", borderwidth=0).grid(row=1, column=0, sticky=NSEW, pady=4)
        tk.Entry(navigation_frame, textvariable=self.playback_frames, width=3, borderwidth=0).grid(row=1, column=1, pady=4)

        navigation_scale_frame = tk.Frame(navigation_frame, borderwidth=0)
        navigation_scale_frame.grid(row=2, column=0, columnspan=2, sticky=NSEW)
        self.navigation_scale = tk.Scale(navigation_scale_frame, from_=0, to=self.data_duration.get(), variable=self.playback_current_time, orient=HORIZONTAL, length=None)
        self.navigation_scale.pack(expand=YES, fill=BOTH)

        navigation_control_frame = tk.Frame(navigation_frame, borderwidth=0)
        navigation_control_frame.grid(row=3, column=0, columnspan=2, sticky=NSEW)
        for x in range(5):
            navigation_control_frame.columnconfigure(x, weight=1)
        tk.Button(navigation_control_frame, text="◁◁", borderwidth=0, command=self.onNavigationBegin).grid(row=0, column=0)
        tk.Button(navigation_control_frame, text="◁", borderwidth=0, command=self.onPreviousFrame).grid(row=0, column=1)
        self.playback_toggle_button = tk.Button(navigation_control_frame, text="▷" if not self.playback_state.get() else "||", borderwidth=0, command=self.onTogglePlayback)
        self.playback_toggle_button.grid(row=0, column=2)
        tk.Button(navigation_control_frame, text="▷", borderwidth=0, command=self.onNextFrame).grid(row=0, column=3)
        tk.Button(navigation_control_frame, text="▷▷", borderwidth=0, command=self.onNavigationEnd).grid(row=0, column=4)

    def onNavigationBegin(self):
        self.playback_current_time.set(0)
        self.update_and_render()

    def onPreviousFrame(self):
        self.playback_current_time.set(max(self.playback_current_time.get()-1, 0))
        self.update_and_render()

    def onTogglePlayback(self):
        if not self.playback_state.get():
            self.playback_state.set(True)
            self.playback_toggle_button.configure(text="||")
            self.playback_handler()
        else:
            self.playback_state.set(False)
            self.playback_toggle_button.configure(text="▷")

    def playback_handler(self):
        if(self.playback_state.get() and self.playback_current_time.get() < self.data_duration.get()):
            try:
                self.playback_current_time.set(min(self.playback_current_time.get()+self.playback_frames.get(), self.data_duration.get()))
            except:
                self.playback_state.set(True)
                self.onTogglePlayback()
            else:
                self.update_and_render()
                self.after(int(1000/int(self.playback_speed.get())), self.playback_handler)

        if(self.playback_current_time.get() >= self.data_duration.get()):
            self.playback_state.set(True)
            self.onTogglePlayback()

    def onNextFrame(self):
        self.playback_current_time.set(min(self.playback_current_time.get()+1, self.data_duration.get()))
        self.update_and_render()

    def onNavigationEnd(self):
        self.playback_current_time.set(self.data_duration.get())
        self.update_and_render()

    def update_and_render(self):
        cdata = self.data_json_obj["keyframes"][str(self.playback_current_time.get())]
        self.data_viewer.add_batch_from_file(cdata)
        self.visualizer.render(self.playback_current_time.get())

    def set_color(self, color_var):
        ret = askcolor()
        if ret:
            color_var.set(ret[1])
            self.draw_widgets()

    def reset(self):
        self.clear_widgets()
        self.draw_widgets()

        self.data_json_obj = None
        self.data_duration.set(0)
        self.data_file_path.set("")

        self.playback_current_time.set(0)
        self.playback_frames.set(1)
        self.playback_state.set(False)
        self.playback_speed.set(1)

        # self.visualizer.reset()

    def onFileSelect(self):
        file_path = askopenfilename(initialdir=os.getcwd(), filetypes=(("JSON 파일(*.json)", "*.json"), ("모든 파일", "*")))
        if file_path:
            self.reset()
            self.data_file_path.set(file_path)
            with open(self.data_file_path.get()) as f:
                self.data_json_obj = json.load(f)
                self.data_duration.set(self.data_json_obj["gamelength"])
            # self.path_label.configure(text="..."+self.data_file_path.get()[-25:])
            self.path_label.configure(text=self.data_file_path.get())
            self.navigation_scale.configure(to=self.data_duration.get())
            self.visualizer.initialize(self.data_json_obj)
            self.update_and_render()

class DataViewer(Treeview):
    def __init__(self, master):
        super().__init__(master, columns=("이름", "X", "Y"))
        self.master = master

        self.column("#0", width=200, stretch=0)
        self.column("#1", width=50, stretch=0)
        self.column("#2", width=50, stretch=0)


        self.heading("#0", text="이름", anchor=W)
        self.heading("#1", text="X", anchor=W)
        self.heading("#2", text="Y", anchor=W)

        self.champion_folder = self.insert("", 1, text="챔피언", values=("", ""), open=True)
        self.camp_folder = self.insert("", 2, text="정글", values=("", ""), open=True)
        self.event_folder = self.insert("", 3, text="이벤트", values=("", ""), open=True)

        #self.insert(self.champion_folder, "end", text="Yasuo", values=("43", "21"))

    def clear_items(self):
        self.delete(*self.get_children())

    def recreate_headers(self):
        self.clear_items()
        self.champion_folder = self.insert("", 1, text="챔피언", values=("", ""))
        self.camp_folder = self.insert("", 2, text="정글", values=("", ""))
        self.event_folder = self.insert("", 3, text="이벤트", values=("", ""))

    def add_champion(self, championname, x, y):
        self.insert(self.champion_folder, END, text=championname, values=(int(x), int(y)))

    def add_batch_from_file(self, keyframe):
        self.recreate_headers()
        for champname, data in keyframe["champ_data"].items():
            avg_coords_x = int((int(data["left"])+int(data["right"]))/2)
            avg_coords_y = int((int(data["top"])+int(data["bottom"]))/2)
            self.insert(self.champion_folder, END, text=champname, values=(avg_coords_x, avg_coords_y))

        for campname, val in keyframe["camp_data"].items():
            if val:
                self.insert(self.camp_folder, END, text=campname, values=("", ""))

        self.item(self.champion_folder, open=True)
        self.item(self.camp_folder, open=True)

if __name__ == '__main__':
    root = tk.Tk()
    handler = ControllerOptionMenu(root)
    handler.draw_widgets()
    root.mainloop()