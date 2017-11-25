# coding=utf-8
"""
@_author:       zhangcaocao
@_website:      http://little-rocket.cn
@_last modified: 2017/11/20
"""
import serial
import time
import thread
import matplotlib.pyplot as plt
import serial.tools.list_ports

data = 0
data_list = []
i = 0

# COM_X = raw_input ('enter comx:')
# USART_BaudRate = raw_input ('enter USART_BaudRate: ')


def Check_Comx():
    plist = list (serial.tools.list_ports.comports ())

    if len (plist) <= 0:
        print("Not Found Comx!!!")
        return 0
    else:
        plist_0 = list (plist[0])
        serialName = plist_0[0]
        serialFd = serial.Serial (serialName, 9600, timeout=60)
        print("Comx:  >>>", serialFd.name)
        return serialFd.name

class MSerialPort:
    message = ''

    # 串口初始化；
    def __init__(self, port, buand):
        self.port = serial.Serial (port, buand)
        if not self.port.isOpen ():
            self.port.open ()

    def port_open(self):
        if not self.port.isOpen ():
            self.port.open ()

    def port_close(self):
        self.port.close ()

    def send_data(self, data):
        number = self.port.write (data)
        return number

    def read_data(self):
        data = self.port.read (1)
        data_list.append (data)
        # print data
        return data

        # data_list.append (mSerial.message)


if __name__ == '__main__':
    COM_X = Check_Comx()
    mSerial = MSerialPort (COM_X, 9600)
    # thread.start_new_thread (mSerial.read_data, ())  # 调用thread模块中的start_new_thread()函数来产生新线程
    Y_lim = raw_input ('enter Y_lim: ')
    while True:
        time.sleep (1 / 30)
        plt.ion ()  # 开启matplotlib的交互模式
        plt.xlim (0, 50)  # 首先得设置一个x轴的区间 这个是必须的
        plt.ylim (-int(Y_lim), int(Y_lim))  # y轴区间
        thread.start_new_thread (mSerial.read_data, ())  # 调用thread模块中的start_new_thread()函数来产生新线程
        # data_list.append (data)
        i = i + 1
        if i > 50:  # 初始状态x轴最大为50
            plt.xlim (i - 50, i)  # 如果当前坐标x已经超过了50，将x的轴的范围右移。
        plt.plot (data_list)  # 将list传入plot画图
        plt.pause (0.01)  # 这个为停顿0.01s，能得到产生实时的效果
