import tkinter as tk
from tkinter import ttk
from IP import send_ip
from UDP import send_UDP
from frame import send_frame


def add_components_to_tab(tab):
    label = tk.Label(tab, text="这是其他函数中创建的组件", bg="white")
    label.grid(row=1, column=0)

def main():
    root = tk.Tk()
    root.geometry("600x500")
    root.title("网络发包")
    # # 创建样式
    # style = ttk.Style(root)
    # # 修改选项卡的背景色
    # style.configure("TNotebook", background='lightblue')
    # style.configure("TNotebook.Tab", background='green')


    # # 创建样式对象并设置选项卡的背景颜色为白色
    style = ttk.Style(root)
    style.configure("TNotebook.Tab", background="white")
    style.configure("TNotebook", background="white")
    style.configure('TFrame', background='white')

    # 创建选项卡控件
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook)
    tab3 = ttk.Frame(notebook)


    notebook.add(tab1, text="发送数据帧")
    notebook.add(tab2, text="发送IP数据包")
    notebook.add(tab3, text="发送UDP数据包")

    # 将选项卡页作为参数传递给函数，将组件添加到选项卡页上
    send_frame(tab1)
    send_ip(tab2)
    send_UDP(tab3)

    root.mainloop()

if __name__ == "__main__":
    main()







