import dataengine as dm
import waveform as wave
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
        imgpath = f"{PATH}/assets/"
        for key, val in image_files.items():
            _path = imgpath + str(val)
            self.photoimages.append(ttk.PhotoImage(name=key, file=_path))

        self.left_panel()
        self.right_panel()

        self.get_load(f'{PATH}/data')

    def left_panel(self):
        """初始化左边"""
        container=ttk.Frame(self,padding=10)
        container.pack(side=LEFT,fill=Y,expand=YES)
        self.plt_view(container)
        self.file_load(container)

    def file_load(self,master):
        """初始化文件读入（左下角）"""
        self.d=f'{PATH}/data'
        self.maxn=0

        self.file_input(master)
        self.Treeview(master)

    def file_input(self,master):
        """初始化路径选择"""
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
        """初始化文件树"""
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
        """选择一个数据"""
        # for item in self.tv.selection():
        #     item_text=self.tv.item(item,"values")
        if self.tv.selection():
            item_text=self.tv.item(self.tv.selection()[0],"values")
            # print(self.d,item_text[0])
            self.draw_pre(item_text[0])

    def get_directory(self):
        """Open dialogue to get directory and update variable"""
        self.update_idletasks()
        if d := askdirectory():
            self.get_load(d)

    def get_load(self,d):
        """载入文件夹"""
        items=self.tv.get_children()
        [self.tv.delete(item)for item in items]
        self.a.clear()
        self.canvas.draw()
        self.d=d

        self.setvar('folder-path', d)
        dirs=os.listdir(d)
        #命名格式xxx_num.csv, 依据num排序
        dirs=[i for i in dirs if len(i.split('.'))>1 and len(i.split('_'))>1 and i.split('.')[1]=="csv"]
        dirs.sort(key=lambda x:int((x.split('_')[1]).split('.')[0]))
        self.maxn = int((dirs[-1].split('_')[1]).split('.')[0])
        for file in dirs:
            # print(d+'/'+file)
            t = os.path.getmtime(f'{d}/{file}')
            timeStruct = time.localtime(t)
            Ttime=time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)
            self.tv.insert('',END,values=(file,Ttime))
        # self.tv.selection_set(len(dirs)-1)

    def plt_view(self,master):
        """初始化图片（左上角）"""
        cv = tk.Canvas(master=master, background='white')
        cv.pack(side=TOP,fill=X,expand=YES)

        f=plt.figure()
        # self.draw_all_from_data(f,"double_1")
        self.a=f.add_subplot(1,1,1)
        self.canvas=FigureCanvasTkAgg(f,master=cv)
        # self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=BOTH,expand=YES)

    def draw_one_from_data(self,X,Y):
        """展示一个峰"""

    def draw_all_from_data(self,X,Y):
        """展示一个数据"""
        # self.a=self.f.add_subplot(1,1,1,ylabel="电压",xlabel="时间")
        self.a.clear()
        self.a.plot(X,Y)
        self.a.set_xlabel("时间/t")
        self.a.set_ylabel("电压/V")
        self.canvas.draw()

    def draw_pre(self,name:str):
        """"""
        # print("dd")
        # print(self.d+'/'+name)
        X = np.arange(2500) * 4e-9
        Y = np.loadtxt(f'{self.d}/{name}')
        self.w_show.y=Y
        self.w_show.process_data()

        self.draw_all_from_data(X,Y)


    def right_panel(self):
        """初始化右边"""
        self.afterid = ttk.StringVar()
        self.running=ttk.BooleanVar(value=False)
        self.init_fou=ttk.BooleanVar(value=False)

        container=ttk.Frame(self,padding=10)
        container.pack(side=LEFT,fill=Y,expand=YES)
        self.data_entry(container)
        self.print_log(container)

    def data_entry(self, master):
        """初始化超参数（右上角）"""
        container=ttk.Frame(master)
        container.pack(side=TOP, fill=X,expand=YES)
        self.noise_threshold=ttk.StringVar(value="")
        self.least_time     =ttk.StringVar(value="")
        self.most_time      =ttk.StringVar(value="")
        self.least_main_peak=ttk.StringVar(value="")
        self.least_sub_peak =ttk.StringVar(value="")
        self.amplify_rate   =ttk.StringVar(value="")
        self.flat_length    =ttk.StringVar(value="")

        self.create_from_entry(container, "噪声门限", self.noise_threshold)
        self.create_from_entry(container, "最小主峰", self.least_main_peak)
        self.create_from_entry(container, "最小次峰", self.least_sub_peak)
        self.create_from_entry(container, "最短衰变时间", self.least_time)
        self.create_from_entry(container, "最长衰变时间", self.most_time)
        self.create_from_entry(container, "主次峰能量比", self.amplify_rate)
        self.create_from_entry(container, "平顶长度", self.flat_length)

        self.Initialize_wave()

        self.craete_buttonbox(container)

    def Initialize_wave(self):
        """"""
        xincr=1e-7
        self.args = {
            "noise_threshold": 0.8,
            "max_peak_num": 8,
            "not_on_line": 1,
            "least_time": 1e-6,
            "most_time": 1e-5,
            "amplify_rate": 0.6,
            # "least_main_peak": 2,
            # "least_sub_peak": 2
        }
        self.w_show= wave.waveform(time_line = xincr, **self.args)
        self.w = wave.waveform(time_line = xincr, **self.args)

    def Initialize_oscilloscope(self):
        """初始化示波器"""
        try:
            self.dms = dm.dataengine(main_scale = '25E-6')
            self.init_fou.set(True)
        except IndexError:
            print(111)

    def create_from_entry(self, master, label, variable):
        """超参数的输入"""
        container=ttk.Frame(master)
        container.pack(fill=X,expand=YES,pady=5)

        lbl=ttk.Label(master=container, text=label.title(),width=15,bootstyle="inverse-info",anchor=CENTER,)
        lbl.pack(side=LEFT, fill=Y,padx=5,expand=YES)

        ent=ttk.Entry(master=container, textvariable=variable)
        ent.pack(side=LEFT, padx=5, fill=X, expand=YES)

    def craete_buttonbox(self,master):
        """超参数的按钮"""
        container=ttk.Frame(master)
        container.pack(fill=X,expand=YES,pady=(15,10))

        sub_btn=ttk.Button(
            master=container,
            text="修改",
            command=self.on_submit,
            bootstyle=SUCCESS,
            width=6,
        )
        sub_btn.pack(side=RIGHT, padx=5,expand=YES)
        # sub_btn.focus_set()

        self.start_btn=ttk.Button(
            master=container,
            text="开始扫描",
            command=self.on_toggle,
            bootstyle=SUCCESS,
            width=8,
        )
        self.start_btn.pack(side=LEFT, padx=5,expand=YES)

    def on_submit(self):
        """修改超参数，判断超参数非法"""
        self.w_show.noise_threshold=self.noise_threshold.get()
        self.w_show.least_time     =self.least_time     .get()
        self.w_show.most_time      =self.most_time      .get()
        self.w_show.least_main_peak=self.least_main_peak.get()
        self.w_show.least_sub_peak =self.least_sub_peak .get()
        self.w_show.amplify_rate   =self.amplify_rate   .get()
        self.w_show.flat_length    =self.flat_length    .get()
        if self.init_fou.get():
            self.w.noise_threshold=self.noise_threshold.get()
            self.w.least_time     =self.least_time     .get()
            self.w.most_time      =self.most_time      .get()
            self.w.least_main_peak=self.least_main_peak.get()
            self.w.least_sub_peak =self.least_sub_peak .get()
            self.w.amplify_rate   =self.amplify_rate   .get()
            self.w.flat_length    =self.flat_length    .get()
        """弹个窗"""

    def print_log(self,master):
        """初始化log（右下角）"""
        style=ttk.Style()
        self.textbox=ttk.ScrolledText(
            master=master,
            highlightcolor=style.colors.primary,
            highlightbackground=style.colors.border,
            highlightthickness=1,
            width=40
        )
        self.textbox.pack(fill=Y,expand=YES)
        default_txt = "( ﾟ∀。)"
        self.textbox.insert(END,default_txt)
        self.textbox.configure(state="disabled")


    def on_toggle(self):
        if not self.init_fou.get() :
            self.Initialize_oscilloscope()
        """模式切换"""
        if self.running.get():
            self.stop_scan()
        else:
            self.start_scan()

    def start_scan(self):
        """开始扫描"""
        self.afterid.set(self.after(1,self.scan))
        self.running.set(True)
        self.start_btn.configure(bootstyle=(DANGER),text="停止扫描")

    def stop_scan(self):
        """停止扫描"""
        self.after_cancel(self.afterid.get())
        self.running.set(False)
        self.start_btn.configure(bootstyle=(SUCCESS),text="开始扫描")

    def scan(self):
        """函数调用，数据写入文件"""
        # print(self.maxn)
        # self.dms.get_data(w)
        self.w.process_data()
        for i in range(w.peaknum):
            tmp = w.peaks[i]
            if tmp["has_second_peak"]:
                self.w.save_waveform(self.d, f"double_{self.d}.csv")
                break
                # plt.scatter([tmp["main_peak"][0], tmp["second_peak"][0]], [tmp["main_peak"][1], tmp["second_peak"][1]], color = 'red')

        """写log"""
        insert_txt = f"( ﾟ∀。){str(self.maxn)}"
        self.textbox.configure(state="normal")
        self.textbox.insert(END,"\n\n")
        self.textbox.insert(END,insert_txt)
        self.textbox.configure(state="disabled")
        self.textbox.yview_moveto(1)

        self.afterid.set(self.after(1000,self.scan))

if __name__ == "__main__":
    app=ttk.Window("Muon")
    Muon(app)
    app.mainloop()