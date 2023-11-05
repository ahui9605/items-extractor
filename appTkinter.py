import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import appExtract as extractor


def get_user_input():
    while True:
        user_input = simpledialog.askstring(" ", "收集机名称:")
        if user_input and user_input.strip():  # 检查输入是否非空且不仅仅包含空白字符
            app.focus_force()  # 强制将焦点设置到主窗口
            return user_input
        else:
            messagebox.showerror("Error", "名称不能为空")


def add_text():
    user_text = text_entry.get()
    if user_text:  # 检查输入是否为空
        if user_text in text_listbox.get(0, tk.END):
            messagebox.showerror("Error", "该名称已添加过，不要重复")
        else:
            text_listbox.insert(tk.END, user_text)
            text_entry.delete(0, tk.END)  # 清空输入框


def get_listbox_items():
    # 获取Listbox中的所有项
    items = text_listbox.get(0, tk.END)
    # 将其转换为Python列表
    items_list = list(items)
    return items_list


def delete_text():
    selected = text_listbox.curselection()
    if selected:
        text_listbox.delete(selected)


def clear_all_text():
    text_listbox.delete(0, tk.END)


def start_script():
    # print(get_listbox_items())
    extractor.main_loop(header=user_text, items=get_listbox_items())


def stop_script():
    pass


app = tk.Tk()
app.title("收集机物品自动提取脚本")

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
window_width = 550
window_height = 600

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

app.geometry(f"{window_width}x{window_height}+{x}+{y}")
# app.resizable(False, False)  # 禁止调整窗口大小


user_text = get_user_input()  # 弹出输入对话框并获取用户输入
print(user_text)  # 打印用户输入的文本，你也可以在程序中的其他地方使用这个变量


# text_entry_label = tk.Label(app, text="收集机物品自动提取脚本")
# text_entry_label.pack(side=tk.TOP, pady=10)


editing_frame = tk.Frame(app)
editing_frame.pack(pady=10)

header_label = tk.Label(editing_frame, text=f"当前收集机为[{user_text}]")
header_label.pack(side=tk.TOP, pady=10)

# ------------------------------------------------------------------------------------
item_input = tk.Frame(editing_frame)
item_input.pack()

text_entry = tk.Entry(item_input, width=30)
text_entry.pack(side=tk.LEFT, padx=5)

add_button = tk.Button(item_input, text="添加物品", command=add_text)
add_button.pack(side=tk.RIGHT, padx=10)

# ------------------------------------------------------------------------------------

listbox_frame = tk.Frame(editing_frame)
listbox_frame.pack(pady=10)

text_listbox = tk.Listbox(listbox_frame, height=10, width=42)
text_listbox.pack(pady=5)

button_frame = tk.Frame(listbox_frame)
button_frame.pack(pady=10)

delete_button = tk.Button(button_frame, text="删除选中", command=delete_text)
delete_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(button_frame, text="全部清空", command=clear_all_text)
clear_button.pack(side=tk.RIGHT, padx=5)


# ------------------------------------------------------------------------------------
script_run = tk.Frame(app)
script_run.pack(side=tk.BOTTOM, pady=5)

start_button = tk.Button(script_run, text="执行脚本", command=start_script)
start_button.pack(side=tk.LEFT, padx=5)

# cancel_button = tk.Button(script_run, text="停止脚本", command=stop_script)
# cancel_button.pack(side=tk.RIGHT, padx=5)
app.mainloop()
