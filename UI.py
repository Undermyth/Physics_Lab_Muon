from analyser import analyse
import dataengine as dm
import waveform as wave
import numpy as np
import datetime
import os
import time
import threading
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter.filedialog import askdirectory
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path
from algorithm import get_curve
matplotlib.rcParams['font.sans-serif']=['SimHei']   # 用黑体显示中文
matplotlib.rcParams['axes.unicode_minus']=False     # 正常显示负号

# PATH = Path(__file__).parent 
PATH=Path().absolute().as_posix()
Golden_ratio=(np.sqrt(5)-1)/2

class Muon(ttk.Frame):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.pack(fill=BOTH,expand=YES)

        image_files = {
            'opened-folder': 'icons8_opened_folder_24px.png',
            # 'window-icon': 'over.png',
        }
        self.photoimages = []
        imgpath = f"{PATH}/assets/"
        for key, val in image_files.items():
            _path = imgpath + str(val)
            self.photoimages.append(ttk.PhotoImage(name=key, file=_path))

        self.left_panel()
        self.right_panel()

        self.get_load(f'{PATH}/data/')

    def left_panel(self):
        """初始化左边"""
        container=ttk.Frame(self,padding=10)
        container.pack(side=LEFT,fill=Y,expand=YES)
        self.plt_view(container)
        self.file_load(container)

    def file_load(self,master):
        """初始化文件读入（左下角）"""
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
        Tv=ttk.Frame(master)
        Tv.pack(side=TOP,fill=X,expand=YES)
        ybar = ttk.Scrollbar(Tv,orient='vertical')
        self.tv = ttk.Treeview(Tv, show='headings', height=5,yscrollcommand=ybar.set)
        ybar['command'] = self.tv.yview
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

        self.tv.pack(side=LEFT,fill=BOTH,expand=YES)
        ybar.pack(side=RIGHT,fill=Y)
        
    def TreeSelect(self,event):
        """选择一个数据"""
        # for item in self.tv.selection():
        #     item_text=self.tv.item(item,"values")
        if self.tv.selection() and not self.analysing:
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
        try:
            self.maxn = int((dirs[-1].split('_')[1]).split('.')[0])
        except Exception:
            self.maxn=0
        for file in dirs:
            # print(d+'/'+file)
            self.load_one(file)
        # self.tv.selection_set(len(dirs)-1)

    def load_one(self,file):
        """添加一个文件"""
        t = os.path.getmtime(self.d+file)
        timeStruct = time.localtime(t)
        Ttime=time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)
        self.tv.insert('',END,values=(file,Ttime))

    def plt_view(self,master):
        """初始化图片（左上角）"""
        cv = tk.Canvas(master=master, background='white')
        cv.pack(side=TOP,fill=X,expand=YES)

        # self.crtl_cv_show=ttk.StringVar(value="缩放")
        self.crtl_cv=ttk.Button(
            master=master,
            bootstyle="success",
            text="",
            command=self.draw_from_data,
            width=30,
        )
        self.crtl_cv.pack(side=TOP,fill=X,expand=YES)
        self.crtl_cv.configure(state='disable')

        f=plt.figure()
        self.a=f.add_subplot(1,1,1)
        self.canvas=FigureCanvasTkAgg(f,master=cv)
        self.canvas.get_tk_widget().pack(fill=BOTH,expand=YES)


    def draw_from_data(self):  # sourcery skip: extract-method
        """展示一个数据, peaknum为全图，[0,peaknum)为子图"""
        # self.a=self.f.add_subplot(1,1,1,ylabel="电压",xlabel="时间")
        self.a.clear()

        if self.show_now==self.w_show.peaknum:
            self.a.plot(self.X,self.Y)
            for peak in self.w_show.peaks:

                if peak["has_second_peak"]:
                    self.a.scatter([peak["main_peak"][0], peak["second_peak"][0]], [peak["main_peak"][1], peak["second_peak"][1]], color="red")
                else:
                    self.a.scatter(peak["main_peak"][0],peak["main_peak"][1],color='orange')
                


        else:
            peak=self.w_show.peaks[self.show_now]

            st=peak["main_peak"][0]-self.args["most_time"]*1.2*(Golden_ratio)
            ed=peak["main_peak"][0]+self.args["most_time"]*1.2
            show_range=np.where((st<self.X) & (self.X<ed))
            self.a.plot(self.X[show_range],self.Y[show_range])
            if peak["has_second_peak"]:
                self.a.scatter([peak["main_peak"][0], peak["second_peak"][0]], [peak["main_peak"][1], peak["second_peak"][1]], color="red")
                a = get_curve.get_curve_a()
                b = np.log(-peak["main_peak"][1]) - a * peak["main_peak"][0]
                def minus_exp(x):
                    return -np.exp(a * x + b)
                xtick = np.linspace(peak["main_peak"][0], peak["main_peak"][0] + 3 * (self.w_show.x[1] - self.w_show.x[0]), 30)
                self.a.plot(xtick, minus_exp(xtick), 'r--')
            else:
                self.a.scatter(peak["main_peak"][0],peak["main_peak"][1],color='orange')
                a = get_curve.get_curve_a()
                b = np.log(-peak["main_peak"][1]) - a * peak["main_peak"][0]
                def minus_exp(x):
                    return -np.exp(a * x + b)
                xtick = np.linspace(peak["main_peak"][0], peak["main_peak"][0] + 3 * (self.w_show.x[1] - self.w_show.x[0]), 30)
                self.a.plot(xtick, minus_exp(xtick), 'r--')

        self.a.set_xlabel("时间/t")
        self.a.set_ylabel("电压/V")
        self.canvas.draw()

        self.show_now= self.show_now+1 if self.show_now<self.w_show.peaknum else 0
        

    def draw_pre(self,name:str):
        """初始化一个数据展示"""
        # print("dd")
        # print(self.d+'/'+name)
        self.X = np.arange(2500) * self.args["time_line"]
        self.Y = np.loadtxt(self.d+name)
        self.w_show.y=self.Y
        self.w_show.process_data()
        # print(self.w_show.peaks)

        self.crtl_cv.configure(state='normal',command=self.draw_from_data,text="缩放")
        # print(self.w_show.peaknum)
        # print(self.w_show.peaks[0]["main_peak"][0]*0.1)

        self.show_now=self.w_show.peaknum
        self.draw_from_data()


    def right_panel(self):
        """初始化右边"""
        # self.afterid = ttk.StringVar()
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

        self.args = {
            "time_line"      : 1e-7,
            "noise_threshold": 0.8,
            "max_peak_num"   : 8,
            "not_on_line"    : 1,
            "least_time"     : 1e-6,
            "most_time"      : 1e-5,
            "amplify_rate"   : 0.6,
            "least_main_peak": 2,
            "least_sub_peak" : 2
        }

        self.noise_threshold=ttk.StringVar(value=self.args["noise_threshold"])
        self.least_time     =ttk.StringVar(value=self.args["least_time"])
        self.most_time      =ttk.StringVar(value=self.args["most_time"])
        self.least_main_peak=ttk.StringVar(value=self.args["least_main_peak"])
        self.least_sub_peak =ttk.StringVar(value=self.args["least_sub_peak"])
        self.amplify_rate   =ttk.StringVar(value=self.args["amplify_rate"])
        # self.flat_length    =ttk.StringVar(value=self.args["flat_length"])

        self.create_from_entry(container, "噪声门限", self.noise_threshold)
        self.create_from_entry(container, "最小主峰", self.least_main_peak)
        self.create_from_entry(container, "最小次峰", self.least_sub_peak)
        self.create_from_entry(container, "最短衰变时间", self.least_time)
        self.create_from_entry(container, "最长衰变时间", self.most_time)
        self.create_from_entry(container, "主次峰能量比", self.amplify_rate)
        # self.create_from_entry(container, "平顶长度", self.flat_length)

        self.Initialize_wave()

        self.craete_buttonbox(container)

    def Initialize_wave(self):
        """初始化波形"""
        self.w_show= wave.waveform(**self.args)
        self.w = wave.waveform(**self.args)

    def Initialize_oscilloscope(self):
        """初始化示波器"""
        try:
            self.dms = dm.dataengine(main_scale = '25E-6')
            self.init_fou.set(True)
            self.insert_log("示波器已初始化完成")
            return 1
        except Exception:
            self.insert_log("示波器初始化失败")
            return 0

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
        self.analysing=0

        ttk.Button(
            master=container,
            text="修改",
            command=self.on_submit,
            bootstyle=SUCCESS,
            width=6,
        ).pack(side=RIGHT, padx=5,expand=YES)

        ttk.Button(
            master=container,
            text="多道扫描",
            # command=self.mul_scan,
            command=lambda: self.thread_it(self.mul_scan),
            bootstyle=SUCCESS,
            width=8,
        ).pack(side=RIGHT, padx=5,expand=YES)

        self.start_btn=ttk.Button(
            master=container,
            text="开始扫描",
            # command=self.on_toggle,
            command=lambda: self.thread_it(self.on_toggle),
            bootstyle=SUCCESS,
            width=8,
        )
        self.start_btn.pack(side=LEFT, padx=5,expand=YES)

    def mul_scan(self):
        """调用多道扫描"""
        if self.running.get():
            self.stop_scan()

        self.insert_log("多道扫描已开始，请耐心等待")

        self.crtl_cv.configure(state='disable',text="")
        self.a.clear()
        self.analysing=1

        self.mainbucket, self.subbucket, avtime, count = analyse(datapath = self.d, channels = 256, max_main_height = 100, max_sub_height = 30, **self.args)
        # print(avtime, count)

        self.show_now=2
        self.switch_bar()
        self.crtl_cv.configure(state='normal',command=self.switch_bar,text="切换")
        self.analysing=0

        self.insert_log(f"多道扫描已完成\n\n共探测到{count}个µ子\n平均衰变时间为{avtime}s")
        
    def switch_bar(self):
        """切换统计图显示"""
        self.a.clear()
        if self.show_now==2:
            b1 = self.a.bar(np.arange(256), self.subbucket)
            b2 = self.a.bar(np.arange(256), self.mainbucket,color='orange')
            self.a.legend([b1, b2], ["电子能量分布", r"$\mu$"+"子能量分布"])
        elif self.show_now==1:
            b2 = self.a.bar(np.arange(256), self.mainbucket,color='orange')
            self.a.legend([b2], [r"$\mu$"+"子能量分布"])
        else:
            b1 = self.a.bar(np.arange(256), self.subbucket)
            self.a.legend([b1], ["电子能量分布"])
        
        self.a.set_xlabel("道数")
        self.a.set_ylabel("计数")
        self.canvas.draw()
        self.show_now= self.show_now+1 if self.show_now<2 else 0

    def on_submit(self):
        if self.running.get() or self.analysing :
            return 
        """修改超参数，判断超参数非法"""
        try:
            self.w_show.noise_threshold=float(self.noise_threshold.get())
            self.w_show.least_time     =float(self.least_time     .get())
            self.w_show.most_time      =float(self.most_time      .get())
            self.w_show.least_main_peak=float(self.least_main_peak.get())
            self.w_show.least_sub_peak =float(self.least_sub_peak .get())
            self.w_show.amplify_rate   =float(self.amplify_rate   .get())
            if self.init_fou.get():
                self.w.noise_threshold=float(self.noise_threshold.get())
                self.w.least_time     =float(self.least_time     .get())
                self.w.most_time      =float(self.most_time      .get())
                self.w.least_main_peak=float(self.least_main_peak.get())
                self.w.least_sub_peak =float(self.least_sub_peak .get())
                self.w.amplify_rate   =float(self.amplify_rate   .get())
            """弹个窗"""
            self.insert_log("参数修改成功")
        except:
            self.insert_log("参数修改失败")

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
        # default_txt = "( ﾟ∀。)"
        default_txt = "已授权访问"
        self.textbox.insert(END,default_txt)
        self.textbox.configure(state="disabled")


    def on_toggle(self):
        if self.analysing:
            return 
        if not self.init_fou.get() and not self.Initialize_oscilloscope():
            return 
        """模式切换"""
        if self.running.get():
            self.stop_scan()
        else:
            self.start_scan()


    def start_scan(self):
        """开始扫描"""
        self.t = threading.Thread(target=self.scan) 
        self.t.start()
        # self.afterid.set(self.after(1000,self.scan))
        self.running.set(True)
        self.start_btn.configure(bootstyle=(DANGER),text="停止扫描")
        self.insert_log("扫描已开始")

    def stop_scan(self):
        """停止扫描"""
        # self.after_cancel(self.afterid.get())
        # threading.Thread._Thread__stop(self.t)
        # self.t.exit()
        self.running.set(False)
        time.sleep(2)
        self.start_btn.configure(bootstyle=(SUCCESS),text="开始扫描")
        self.insert_log("扫描已终止")

    def scan(self):
        """函数调用，数据写入文件"""
        cnt=0
        while 1:
            # print(self.maxn)
            self.dms.get_data(self.w)
            self.w.process_data()
            for i in range(self.w.peaknum):
                tmp = self.w.peaks[i]
                if tmp["has_second_peak"]:
                    self.maxn+=1
                    self.w.save_waveform(self.d, f"double_{self.maxn}.csv")
                    self.load_one(f"double_{self.maxn}.csv")
                    self.draw_pre(f"double_{self.maxn}.csv")
                    break
                    # plt.scatter([tmp["main_peak"][0], tmp["second_peak"][0]], [tmp["main_peak"][1], tmp["second_peak"][1]], color = 'red')

            """写log"""
            # self.insert_log(f"( ﾟ∀。){str(self.maxn)}")
            cnt+=1
            self.insert_log(f"已完成{cnt}次扫描，累计探测双峰{str(self.maxn)}个")

            if not self.running.get():
                break
        # self.afterid.set(self.after(1000,self.scan))

    def insert_log(self,insert_txt):
        """写入log"""
        self.textbox.configure(state="normal")
        self.textbox.insert(END,"\n\n")
        self.textbox.insert(END,insert_txt)
        self.textbox.configure(state="disabled")
        self.textbox.yview_moveto(1)

    @staticmethod
    def thread_it(func, *args):
        """多线程，防止控件卡住"""
        t = threading.Thread(target=func, args=args) 
        #t.setDaemon(True)  # 守护--就算主界面关闭，线程也会留守后台运行
        t.start()      # 启动
        # t.join()     # 阻塞--会卡死界面！

if __name__ == "__main__":
    app=ttk.Window(
        title="Muon",
        iconphoto=f"{PATH}/assets/over.png"
    )
    Muon(app)
    app.mainloop()