#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#from tkinter import Tk
import tkinter
from tkinter import ttk
from tkinter import filedialog
from time import sleep

from controller import *

class GUI(ttk.Frame):
    def __init__(self, parent, *args, **kwargs): 
        ttk.Frame.__init__(self, parent, *args, **kwargs) 
        self.root = parent 
        self.progress = 0.0
        self.show = None
        self.intensity = 100
        self.period = {"dia": 1, "semana": 7, "mes": 30}
        self.init_gui() 

    def init_gui(self):
        self.root.title('Dispersão do Poluente')
        self.content = ttk.Frame(self.root, padding=(3,3,12,12), width=1200)
        self.content.grid(column=3, row=0, sticky="nsw")#(N, S, E, W))

        self.frame = ttk.Frame(self.root, borderwidth=5, relief="sunken", width=800, height=800)
        self.frame.grid(column=0, row=0, columnspan=3, sticky="nse")

        self.lbl_map = ttk.Label(self.content, text="Malha do mapa:")
        self.lbl_map.grid(column=3, row=2, columnspan=2, padx=10, pady=1, sticky="nw")
        self.path_entry = ttk.Entry(self.content)
        self.path_entry.grid(column=5, row=2, columnspan=2, pady=1, sticky="nw")
        self.btn_browser = ttk.Button(self.content, text="Carregar", command=self.browserFile)
        self.btn_browser.grid(column=7, row=2, columnspan=2, padx=10, pady=1, sticky="ne")

        self.lbl_intensity = ttk.Label(self.content, text="Intensidade da Fonte:")
        self.lbl_intensity.grid(column=3, row=3, columnspan=2, padx=10, sticky="nw")
        self.intensity_entry = ttk.Entry(self.content)
        self.intensity_entry.grid(column=5, row=3, columnspan=2, sticky="nw")

        self.lbl_point = ttk.Label(self.content, text="Coordenadas (x,y):")
        self.lbl_point.grid(column=3, row=4, columnspan=2, padx=10, pady=9, sticky="nw")
        self.point_entry = ttk.Entry(self.content)
        self.point_entry.grid(column=5, row=4, columnspan=2, pady=9, sticky="nw")

        self.lbl_interval = ttk.Label(self.content, text="Gravar por:")
        self.lbl_interval.grid(column=3, row=5, columnspan=2, padx=10, pady=1, sticky="nw")
        self.interval_entry = ttk.Entry(self.content)
        self.interval_entry.grid(column=5, row=5, columnspan=2, pady=1, sticky="nw")

        self.lbl_cicles = ttk.Label(self.content, text="Número de interações:")
        self.lbl_cicles.grid(column=3, row=6, padx=10, pady=9, sticky="nw")
        self.cicles_entry = ttk.Entry(self.content)
        self.cicles_entry.grid(column=5, row=6, pady=9, sticky="nw")

        self.lbl_progress = ttk.Label(self.content, text="Progresso {:0.1f}%".format(self.progress), font=("Helvetica", 16))
        self.lbl_progress.grid(column=3, row=7, padx=10, pady=30, sticky="new")

        self.btn_start = ttk.Button(self.content, text="Iniciar simulação", command=self.onStart)
        self.btn_start.grid(column=3, row=10, columnspan=2, padx=10, pady=10, sticky="nw")
        self.btn_finish = ttk.Button(self.content, text="Encerrar simulação", command=self.onStart)
        self.btn_finish.grid(column=5, row=10, columnspan=2, padx=10, pady=10, sticky="nw")
        
    def onStart(self):
        f = open(".default.config")
        default = f.readlines()
        f.close()
        
        self.progress = 0.0
        
        self.intensity = self.intensity_entry.get()
        if(self.intensity == ""):
            self.intensity = default[1].strip()

        self.intensity = float(self.intensity)

        if(self.point_entry.get() == ""):
            self.point = default[2].strip().split(",")
        else:
            self.point = self.point_entry.get().split(",")
        print(self.point)

        path = self.path_entry.get()
        if(path == ""):
            path = default[0].strip()
            
        if(self.interval_entry.get() == ""):
            interval = self.period[default[3].strip()]
        else:
            interval = self.period[self.interval_entry.get()]

        cicles = self.cicles_entry.get()
        if(cicles == ""):
            cicles = default[4].strip()

        cicles = int(cicles)

        for widget in self.frame.winfo_children():
            widget.destroy()
        
        self.map = Control(interval, cicles, self.intensity, path, tuple(self.point))
        self.show = self.createMap()

        self.toShow()
        return self.show
    
    def toShow(self):
        w = 800/self.map.columns
        h = 800/self.map.lines

        for cmap in self.map.cache:
            for i in range(0, self.map.lines):
                for j in range(0, self.map.columns):
                    value = int(150-(150*(cmap[i][j]/self.intensity)))
                    color = '#%02x%02x%02x' % (value,value,value)
                    if(cmap[i][j]>0):
                        self.show[i][j].destroy()
                        self.show[i][j] = tkinter.Frame(self.frame, borderwidth=1, relief="sunken", width=w, height=h,bg=color)
                        self.show[i][j].grid(column=j, row=i)

    def createMap(self):
        frames = [[0]*self.map.columns for i in range (0,self.map.lines)]
        back = ["#0000FF", "#00FF00"]
        w = 800/self.map.columns
        h = 800/self.map.lines

        for i in range(0, self.map.lines):
            for j in range(0, self.map.columns):
                frames[i][j] = tkinter.Frame(self.frame, borderwidth=1, relief="sunken", width=w, height=h,bg=back[int(self.map.MAP[i][j])])
                frames[i][j].grid(column=j, row=i)
        return frames

    def browserFile(self):
            filename =  filedialog.askopenfilename(initialdir = "~/",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
            self.path_entry.delete(0)
            self.path_entry.insert(0, filename)
            return filename

if __name__ == '__main__': 
    root = tkinter.Tk()
    GUI(root) 
    root.mainloop()
