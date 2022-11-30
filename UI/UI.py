import numpy as np
import datetime
import os
import time
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter.filedialog import askdirectory
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path
matplotlib.rcParams['font.sans-serif']=['SimHei']   # 用黑体显示中文
matplotlib.rcParams['axes.unicode_minus']=False     # 正常显示负号

# PATH = Path(__file__).parent 
PATH=Path().absolute().as_posix()

class Muon(ttk.Frame):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.pack(fill=BOTH,expand=YES)

        image_files = {
            'opened-folder': 'icons8_opened_folder_24px.png',
        }
        self.photoimages = []
        imgpath = PATH + "/assets/"
        for key, val in image_files.items():
            _path = imgpath + str(val)
            self.photoimages.append(ttk.PhotoImage(name=key, file=_path))

        self.left_panel()
        self.right_panel()

        self.get_load(PATH + '/data')

    def left_panel(self):
        """"""
        container=ttk.Frame(self,padding=10)
        container.pack(fill=Y,expand=YES)
        self.plt_view(container)
        self.file_load(container)

    def file_load(self,master):
        """"""
        self.file_input(master)
        self.Treeview(master)

    def file_input(self,master):
        """"""
        browse_frm=ttk.Frame(master)
        browse_frm.pack(side=TOP,fill=X,expand=YES)

        file_entry=ttk.Entry(browse_frm,textvariable='folder-path',state="readonly")
        file_entry.pack(side=LEFT, fill=X, expand=YES)
        btn = ttk.Button(
            master=browse_frm, 
            image='opened-folder', 
            bootstyle=(LINK, SECONDARY),
            command=self.get_directory
        )
        btn.pack(side=RIGHT)

    def Treeview(self,master):
        """"""
        self.tv = ttk.Treeview(master, show='headings', height=5)
        self.tv.configure(
            columns=(
                "name","time"
            )
        )

        for col in self.tv['columns']:
            self.tv.column(col, stretch=False)
            self.tv.heading(col, text=col.title(), anchor=W)

        self.tv.column("name",width=100,stretch=True)

        self.tv.bind('<Double-Button-1>',self.TreeSelect)

        self.tv.pack(side=TOP,fill=X,expand=YES)
        
    def TreeSelect(self,event):
        """"""
        # for item in self.tv.selection():
        #     item_text=self.tv.item(item,"values")
        if self.tv.selection():
            item_text=self.tv.item(self.tv.selection()[0],"values")
            # print(self.d,item_text[0])
            self.draw_all_from_data(item_text[0])

    def get_directory(self):
        """Open dialogue to get directory and update variable"""
        self.update_idletasks()
        if d := askdirectory():
            self.get_load(d)

    def get_load(self,d):
        """"""
        self.d=d
        items=self.tv.get_children()
        [self.tv.delete(item)for item in items]
        self.a.clear()
        self.canvas.draw()

        self.setvar('folder-path', d)
        dirs=os.listdir(d)
        #命名格式xxx_num.csv, 依据num排序
        dirs=[i for i in dirs if len(i.split('.'))>1 and len(i.split('_'))>1 and i.split('.')[1]=="csv"]
        dirs.sort(key=lambda x:int((x.split('_')[1]).split('.')[0]))
        for file in dirs:
            # print(d+'/'+file)
            t = os.path.getmtime(d+'/'+file)
            timeStruct = time.localtime(t)
            Ttime=time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)
            self.tv.insert('',END,values=(file,Ttime))
        # self.tv.selection_set(len(dirs)-1)

    def plt_view(self,master):
        """"""
        cv = tk.Canvas(master=master, background='white')
        cv.pack(side=TOP,fill=X,expand=YES)

        f=plt.figure()
        # self.draw_all_from_data(f,"double_1")
        self.a=f.add_subplot(1,1,1)
        self.canvas=FigureCanvasTkAgg(f,master=cv)
        # self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=BOTH,expand=YES)

    def drwa_one_from_data(self):
        """"""

    def draw_all_from_data(self,name:str):
        """"""
        # print("dd")
        # print(self.d+'/'+name)
        X = np.arange(2500) * 4e-9
        Y = np.loadtxt(self.d+'/'+name)

        # self.a=self.f.add_subplot(1,1,1,ylabel="电压",xlabel="时间")
        self.a.clear()
        self.a.plot(X,Y)
        self.a.set_xlabel("时间/t")
        self.a.set_ylabel("电压/V")
        self.canvas.draw()


    def right_panel(self):
        """"""


if __name__ == "__main__":
    app=ttk.Window("Muon")
    Muon(app)
    app.mainloop()