import tkinter as tk
from telnetlib import IP
from tkinter import messagebox
from scapy.all import *

def send_ip(tab):
    def check_integer_input(input_str):
        try:
            int(input_str)
            return True
        except ValueError:
            return False

    def toggle_packet_length_entry():
        if fragment_var.get():
            packet_length_label.grid(row=6, column=0, padx=10, pady=5)
            packet_length_entry.grid(row=6, column=1, padx=10, pady=5)
        else:
            packet_length_label.grid_forget()
            packet_length_entry.grid_forget()

    def send_ip_packet():
        # 获取用户输入的参数
        source_ip = source_ip_entry.get()
        destination_ip = destination_ip_entry.get()
        payload_text = payload_entry.get("1.0", "end-1c")
        payload = payload_text.encode('utf-8')
        fragment = fragment_var.get()

        ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
        if not re.match(ip_pattern, source_ip):
            messagebox.showerror("错误", "源IP地址格式不正确，请按照xxx.xxx.xxx.xxx的格式输入")
            return
        if not re.match(ip_pattern, destination_ip):
            messagebox.showerror("错误", "目标IP地址格式不正确，请按照xxx.xxx.xxx.xxx的格式输入")
            return
        if not check_integer_input(custom_flags_entry.get()):
            messagebox.showerror("错误", "请输入一个有效的协议标志（整数）")
            return
        custom_flags = int(custom_flags_entry.get())
        if custom_flags > 255:
            messagebox.showerror("错误", "请输入一个有效的协议标志（小于256）")
            return

        # 获取用户输入的数据包长度
        packet_length = packet_length_entry.get()
        if fragment and not check_integer_input(packet_length):
            messagebox.showerror("错误", "请输入一个有效的数据包长度（整数）")
            return
        if not packet_length:
            packet_length = 0
        packet_length = int(packet_length)

        if packet_length > 65535:
            messagebox.showerror("错误", "请输入一个有效的数据包长度（0~65535）")
            return

        # 如果没有输入数据，则自动生成一些数据
        if not payload:
            payload = "Hello IP!"

        # 构造IP数据包并发送
        send_ip_packet_with_params(source_ip, destination_ip, payload, fragment, custom_flags, packet_length)

    def send_ip_packet_with_params(source_ip, destination_ip, payload, fragment=False, custom_flags=0,
                                   packet_length=0):
        # 构造IP头部
        ip_header = IP(src=source_ip, dst=destination_ip, flags="MF" if fragment else "DF", frag=0)

        # 设置自定义的协议标志
        ip_header.proto = custom_flags

        # 如果数据包长度设置，则添加相关选项
        if packet_length:
            # 计算数据包需要分片的数量
            num_fragments = int(math.ceil(len(payload) / float(packet_length)))
            # 设置分片标志和总长度
            ip_header.flags = "MF"
            ip_header.len = packet_length
        else:
            num_fragments = 1

        # 发送数据包
        if fragment:
            for i in range(num_fragments):
                if packet_length:
                    fragment_payload = payload[i * packet_length: (i + 1) * packet_length]
                else:
                    fragment_payload = payload
                # 设置分片偏移
                ip_header.frag = i * (packet_length // 8)
                send(ip_header / fragment_payload)
        else:
            # 直接发送整个数据载荷
            send(ip_header / payload)
    # 添加输入字段和标签
    source_ip_label = tk.Label(tab, text="源IP地址:", bg="white")
    source_ip_label.grid(row=1, column=0, padx=10, pady=5)
    source_ip_entry = tk.Entry(tab, highlightbackground="black", highlightcolor="black", highlightthickness=1)
    source_ip_entry.grid(row=1, column=1, padx=10, pady=5)

    destination_ip_label = tk.Label(tab, text="目标IP地址:", bg="white")
    destination_ip_label.grid(row=1, column=2, padx=10, pady=5)
    destination_ip_entry = tk.Entry(tab, highlightbackground="black", highlightcolor="black", highlightthickness=1)
    destination_ip_entry.grid(row=1, column=3, padx=10, pady=5)

    custom_flags_label = tk.Label(tab, text="协议标志:", bg="white")
    custom_flags_label.grid(row=2, column=0, padx=10, pady=5)
    custom_flags_entry = tk.Entry(tab, highlightbackground="black", highlightcolor="black", highlightthickness=1)
    custom_flags_entry.grid(row=2, column=1, padx=10, pady=5)

    packet_length_label = tk.Label(tab, text="数据包长度:", bg="white")
    packet_length_entry = tk.Entry(tab, highlightbackground="black", highlightcolor="black", highlightthickness=1)
    fragment_var = tk.BooleanVar()
    fragment_var.set(False)
    fragment_checkbutton = tk.Checkbutton(tab, text="是否分片", variable=fragment_var,
                                          command=toggle_packet_length_entry, bg="white")
    fragment_checkbutton.grid(row=5, column=0, padx=10, pady=5)  # 调整位置

    payload_label = tk.Label(tab, text="数据:", bg="white")
    payload_label.grid(row=3, column=0, padx=10, pady=5, rowspan=2)  # 将 rowspan 设置为2

    payload_entry = tk.Text(tab, width=60, height=20, highlightbackground="black", highlightcolor="black", highlightthickness=1)
    payload_entry.grid(row=3, column=1, columnspan=3, padx=10, pady=5)  # 这里不需要 rowspan

    send_button = tk.Button(tab, text="发送IP数据包", command=send_ip_packet, bg="white")
    send_button.grid(row=9, column=0, columnspan=2)
