import tkinter as tk
from tkinter import messagebox
import re

import scapy.all
from scapy.layers.l2 import Ether


def send_frame(tab):
    def send_custom_frame():
        # 获取用户输入的参数
        source_mac = source_mac_entry.get()
        destination_mac = destination_mac_entry.get()
        payload_text = payload_entry.get("1.0", "end-1c")
        payload = payload_text.encode('utf-8')

        if not custom_protocol_entry.get():
            custom_protocol = 1
        else:
            custom_protocol = int(custom_protocol_entry.get(), 16)

        mac_pattern = r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$'
        if not re.match(mac_pattern, source_mac):
            messagebox.showerror("错误", "请输入一个有效的源MAC地址（01:23:45:67:89:ab）")
            return
        if not re.match(mac_pattern, destination_mac):
            messagebox.showerror("错误", "请输入一个有效的目标MAC地址（01:23:45:67:89:ab）")
            return

        if custom_protocol > int('FFFF', 16):
            messagebox.showerror("错误", "请输入一个有效的协议标志（小于FFFF）")
            return

        # 如果没有输入数据，则自动生成一些数据
        if not payload:
            data = "Hello FRAME!"
        # 构造以太网帧
        frame = Ether(src=source_mac, dst=destination_mac, type=custom_protocol) / payload

        # 发送数据帧
        scapy.all.sendp(frame)


    # 创建并布局界面组件
    source_mac_label = tk.Label(tab, text="源MAC地址:", bg="white")
    source_mac_label.grid(row=1, column=0, pady=5)
    source_mac_entry = tk.Entry(tab, highlightbackground="black", highlightcolor="black", highlightthickness=1)
    source_mac_entry.grid(row=1, column=1, pady=5)

    destination_mac_label = tk.Label(tab, text="目标MAC地址:", bg="white")
    destination_mac_label.grid(row=1, column=2, pady=5)
    destination_mac_entry = tk.Entry(tab, highlightbackground="black", highlightcolor="black", highlightthickness=1)
    destination_mac_entry.grid(row=1, column=3, pady=5)

    custom_protocol_label = tk.Label(tab, text="自定义协议标志:", bg="white")
    custom_protocol_label.grid(row=2, column=0, pady=5)
    custom_protocol_entry = tk.Entry(tab, highlightbackground="black", highlightcolor="black", highlightthickness=1)
    custom_protocol_entry.grid(row=2, column=1, pady=5)

    payload_label = tk.Label(tab, text="数据:", bg="white")
    payload_label.grid(row=3, column=0, pady=5)
    payload_entry = tk.Text(tab, width=60, height=25, highlightbackground="black", highlightcolor="black", highlightthickness=1)
    payload_entry.grid(row=3, column=1, columnspan=3, pady=5)

    send_button = tk.Button(tab, text="发送数据帧", command=send_custom_frame, bg="white")
    send_button.grid(row=5, column=0, columnspan=2, pady=5)
