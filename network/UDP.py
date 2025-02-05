import tkinter as tk
from telnetlib import IP
from tkinter import messagebox, ttk
from scapy.all import *
from scapy.layers.inet import UDP
from scapy.layers.l2 import Ether


def send_UDP(tab):
    def send_udp_packet():
        # 获取用户输入的参数
        source_mac = source_mac_entry.get()
        destination_mac = destination_mac_entry.get()
        source_ip = source_ip_entry.get()
        destination_ip = destination_ip_entry.get()
        if not source_port_entry.get():
            source_port = 8080
        else:
            source_port = int(source_port_entry.get())
        if not destination_port_entry.get():
            destination_port = 8090
        else:
            destination_port = int(destination_port_entry.get())

        data_text = data_entry.get("1.0", "end-1c")
        data = data_text.encode('utf-8')

        ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
        if not re.match(ip_pattern, source_ip):
            messagebox.showerror("错误", "源IP地址格式不正确，请按照xxx.xxx.xxx.xxx的格式输入")
            return
        if not re.match(ip_pattern, destination_ip):
            messagebox.showerror("错误", "目标IP地址格式不正确，请按照xxx.xxx.xxx.xxx的格式输入")
            return

        mac_pattern = r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$'
        if not re.match(mac_pattern, source_mac):
            messagebox.showerror("错误", "请输入一个有效的源MAC地址（01:23:45:67:89:ab）")
            return
        if not re.match(mac_pattern, destination_mac):
            messagebox.showerror("错误", "请输入一个有效的目标MAC地址（01:23:45:67:89:ab）")
            return


        # 如果没有输入数据，则自动生成一些数据
        if not data:
            data = "Hello UDP!"

        # 构造 UDP 数据包
        udp_packet = Ether(src=source_mac, dst=destination_mac) / \
                     IP(src=source_ip, dst=destination_ip) / \
                     UDP(sport=source_port, dport=destination_port) / \
                     data

        # 发送 UDP 数据包
        sendp(udp_packet)
        messagebox.showinfo("Success", "UDP数据包已发送！")

    # 创建并布局界面组件
    source_mac_label = tk.Label(tab, text="源MAC地址:", bg="white")
    source_mac_label.grid(row=1, column=0, pady=5)
    source_mac_entry = tk.Entry(tab, highlightbackground="black", highlightcolor="black", highlightthickness=1)
    source_mac_entry.grid(row=1, column=1, pady=5)

    destination_mac_label = tk.Label(tab, text="目的MAC地址:", bg="white")
    destination_mac_label.grid(row=1, column=2, pady=5)
    destination_mac_entry = tk.Entry(tab, highlightbackground="black", highlightcolor="black", highlightthickness=1)
    destination_mac_entry.grid(row=1, column=3, pady=5)

    source_ip_label = tk.Label(tab, text="源IP地址:", bg="white")
    source_ip_label.grid(row=2, column=0, pady=5)
    source_ip_entry = tk.Entry(tab, highlightbackground="black", highlightcolor="black", highlightthickness=1)
    source_ip_entry.grid(row=2, column=1, pady=5)

    destination_ip_label = tk.Label(tab, text="目的IP地址:", bg="white")
    destination_ip_label.grid(row=2, column=2, pady=5)
    destination_ip_entry = tk.Entry(tab, highlightbackground="black", highlightcolor="black", highlightthickness=1)
    destination_ip_entry.grid(row=2, column=3, pady=5)

    source_port_label = tk.Label(tab, text="源端口号:", bg="white")
    source_port_label.grid(row=3, column=0, pady=5)
    source_port_entry = tk.Entry(tab, highlightbackground="black", highlightcolor="black", highlightthickness=1)
    source_port_entry.grid(row=3, column=1, pady=5)

    destination_port_label = tk.Label(tab, text="目的端口号:", bg="white")
    destination_port_label.grid(row=3, column=2, pady=5)
    destination_port_entry = tk.Entry(tab, highlightbackground="black", highlightcolor="black", highlightthickness=1)
    destination_port_entry.grid(row=3, column=3, pady=5)

    data_label = tk.Label(tab, text="数据:", bg="white")
    data_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")


    # 创建一个多行输入框
    data_entry = tk.Text(tab, width=60, height=23, highlightbackground="black", highlightcolor="black", highlightthickness=1)  # 设置宽度和高度（行数）
    data_entry.grid(row=4, column=1, columnspan=3, padx=10, pady=5, sticky="ew")  # 设置 columnspan 参数

    send_button = tk.Button(tab, text="发送UDP数据包", command=send_udp_packet, bg="white")
    send_button.grid(row=5, column=0, columnspan=3, pady=5)

