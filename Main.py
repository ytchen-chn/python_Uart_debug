# coding=utf-8
"""
@_author:       zhangcaocao
@_website:      http://little-rocket.cn
@_last modified: 2017/11/21
"""


import serial
import time
import thread
import threading
import Queue
import matplotlib.pyplot as plt
import serial.tools.list_ports
from Tkinter import *
import random
import sys


data_list = []
showdata  = []
i         = 0
len1 = 0
len2 = 0
is_empty = True

ABOUT_MESSAGE = '''
    Author       : zhangcaolin
    Author_email : zhangcaocao66@gmail.com
    Blog         : http://little-rocket.cn/
    Version      : 1.0
    '''

# queue = Queue.Queue(3)
# 检查，扫描，Comx； 默认波特率为9600
def Check_Comx():
    plist = list (serial.tools.list_ports.comports ())

    if len (plist) <= 0:
        print("Not Found Comx!!!")
        return 0
    else:
        plist_0 = list (plist[0])
        serialName = plist_0[0]
        serialFd = serial.Serial (serialName, 9600, timeout=1)
        print(u"扫描到： ", serialFd.name)
        return serialFd.name

def Check_lendatelist_change():
    len1 = len(data_list)
    time.sleep(0.1)
    len2 = len(data_list)
    if (len1 < len2) & (len2 != 0):
        len1 = 0
        len2 = 0
        return True
    else:
        len1 = 0
        len2 = 0
        return False

def Drawing_only():
    Y_lim = 10
    i = 0
    while True:
        plt.ion ()  # 开启matplotlib的交互模式
        plt.xlim (0, 50)  # 首先得设置一个x轴的区间 这个是必须的
        plt.ylim (-int (Y_lim), int (Y_lim))  # y轴区间
            # thread.start_new_thread (mSerial.read_data, ())  # 调用thread模块中的start_new_thread()函数来产生新线程
        if Check_lendatelist_change() == True:
            i = i + 1
            if i > 50:  # 初始状态x轴最大为50
                plt.xlim (i - 50, i)  # 如果当前坐标x已经超过了50，将x的轴的范围右移。
            plt.plot (data_list)  # 将list传入plot画图
            plt.pause (0.01)  # 这个为停顿0.01s，能得到产生实时的效果


def Drawing():
    mSerial = MSerialPort ()
    Y_lim = 10
    i = 0
    while True:
        plt.ion ()  # 开启matplotlib的交互模式
        plt.xlim (0, 50)  # 首先得设置一个x轴的区间 这个是必须的
        plt.ylim (-int (Y_lim), int (Y_lim))  # y轴区间
        thread.start_new_thread (mSerial.read_data, ())  # 调用thread模块中的start_new_thread()函数来产生新线程
        if Check_lendatelist_change() == True:
            i = i + 1
            if i > 50:  # 初始状态x轴最大为50
                plt.xlim (i - 50, i)  # 如果当前坐标x已经超过了50，将x的轴的范围右移。
            plt.plot (data_list)  # 将list传入plot画图
            plt.pause (0.01)  # 这个为停顿0.01s，能得到产生实时的效果
        else:
            plt.close ('all')
            thread.exit()
            sys.exit()


def Help_About_menu():
    '''Help-About IDEL function'''
    label = Label (root, text=ABOUT_MESSAGE, fg='red')
    label.pack (side='top')
data = 0
class MSerialPort:
    def __init__(self, myBaudrate=9600, myTimeout=1):
        try:
            Com_X = Check_Comx()
            self.ser = serial.Serial (port=Com_X, baudrate=myBaudrate, bytesize=8,
                                      timeout=myTimeout)  # set the timeout = 1 second
        except:
            print "upper Computer<<<Error: Failed to Open COM!"
            sys.exit ()

    # 发送数据
    def send_data(self, data):
        self.ser.open()
        number = self.ser.write (data)
        return number

    # 读取数据，
    def read_data(self):
        data = int(self.ser.read(1))
        data_list.append (data)
        return  data

    def close_port(self):
        self.ser.close()

class GUI (Frame):
    def __init__(self, master, **kw):

        Frame.__init__ (self, master, **kw)
        frame = Frame (master)
        frame.pack ()

        # 输出框提示
        self.lab3 = Label (frame, text='Date Show')
        self.lab3.grid (row=0, column=1, sticky=W)
        # 输出框
        self.show = Text (frame, width=90, height=30, wrap=WORD)
        self.show.grid (row=1, column=1, rowspan=4, sticky=W)

        # 数据显示按钮
        self.button3 = Button (frame, text='Display Data....', command=self.Data_Display)
        self.button3.grid (row=2, column=0, sticky=W)

        # 图像显示按钮
        self.button4 = Button (frame, text='Display image..', command=self.Display_image)
        self.button4.grid (row=3, column=0, sticky=W)


        # 串口信息提示框
        self.lab4 = Label(frame, text='Message Show')
        self.lab4.grid(row=6,column=0, sticky=W)
        self.showSerial = Text (frame, width=30, height=2, wrap=WORD)
        self.showSerial.grid (row=11, column=0, sticky=W)

        # 添加菜单
        menubar = Menu (master)

        filemenu = Menu (menubar, tearoff=0)
        menubar.add_cascade (label='File', menu=filemenu)
        filemenu.add_command (label='Exit', command=master.quit)

        editmenu = Menu (menubar, tearoff=0)
        menubar.add_cascade (label='Help', menu=editmenu)
        editmenu.add_command (label='About', command=Help_About_menu)
        master.config (menu=menubar)

    # 数据显示
    def Data_Display(self):
        n = 0
        listchangeflag = True
        listchangeflag = Check_lendatelist_change()
        self.showSerial.delete (0.0, END)
        self.showSerial.insert (0.0, "Data_Display")
        while True:
            if  listchangeflag == True & n < len(data_list):
                data = data_list[n]
                self.show.insert(0.0, data)
                n = n + 1
            else:
                time.sleep(1)
                listchangeflag = Check_lendatelist_change()
    # 图像显示
    def Display_image(self):
        thread.start_new_thread (Drawing, ())  # 调用thread模块中的start_new_thread()函数来产生新线程

if __name__ == "__main__":
    root = Tk ()
    root.title ("Serial GUI")
    root.geometry("900x630")
    app = GUI (root)
    root.mainloop ()