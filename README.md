# Physics_Lab_Muon
Muon detection lab code for 2022 Autumn

<img src="/Users/a/Desktop/program/2211/github-desktop/Muon_final/icon.JPG" alt="icon" style="zoom:50%;" />

本次实验已完结

我估计ck懒得写这个，所以我还是多写一点吧。

写给后来的同学的一点说明：

这里是2022秋冬学期的$\mu$子测量实验的代码仓库。我们全是用python写的，建议不要像20级一样用C++去写，C++看起来一坨答辩。如果没有OOP基础的话建议也不要去读20级的代码，很花时间并且很难看懂，甚至不如自己重写一套。

我们的这些代码应该还是可以复用的。很多模块下面都有__main__函数，里面有怎么使用的示例。test.py里面有完整的采集过程的示例。寻峰算法独立在algorithm/search.py里面，不过版本有点乱，还有一个serach不知道是什么东西，我在质问ck了（）。UI.py是图形界面单独的东西，也就是说可以在不改动后端代码的前提下换GUI的前端。峰修正的代码主要在algorithm/peak_fix.py和algorithm/check_shape.py里面。

哦，另外也建议没事不要去用Qt。Qt工程量比较大，可能我们用的ttkbootstrap会好一点。~~不过ck写的寻峰和GUI现在都是一坨屎山，我估计也很难改~~

友情提示，这个实验的速度瓶颈依然在于示波器传输太慢。如果会FPGA的话可以试试，不过我觉得使用那个多道分析仪的希望更大一些。我把我们的论文也放上来。论文很长，两篇论文大部分内容是一样的，差异比较多的部分在第四部分，我的比较偏重峰值修正，ck的比较偏重寻峰。可以参考参考。

模拟的话，我们不会。找模拟的去。

没辣！祝各位好运！仓库我待会会整理整理。联系方式：3290402927@qq.com(我的)，Tian42chen@gmail.com(ck的)

Completed in Dec 31st, 2022

ps, happy new year
