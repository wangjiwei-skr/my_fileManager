# -*- coding:utf8 -*- # 避免中文乱码

import os
import tkinter
import tkinter.messagebox
from xml_tool import XmlTool
import pyperclip


change_file_name = []
label_list = []
xmltool = XmlTool()

def open_file(arg):
    try:
        messages = xmltool.read_message()
        start_directory = messages[arg]['file_path']
        start_up_file = start_directory.split('\\')[-1]
        if start_up_file.split('.')[-1] in ["bat", "exe"] and len(start_up_file.split('.')) == 2:
            os.chdir(os.path.dirname(start_directory))
            os.system(start_up_file)
        else:
            os.startfile(start_directory)
    except Exception as e:
        tkinter.messagebox.showinfo('提示', '地址不存在')


def copy_file_path(arg):
    messages = xmltool.read_message()
    start_directory = messages[arg]['file_path']
    pyperclip.copy(start_directory)


def copy_file_path_p4(arg):
    messages = xmltool.read_message()
    start_directory = messages[arg]['file_path'].split('exe\\')
    print(start_directory)
    if len(start_directory)==2:
        p4_place = start_directory[-1].replace('\\','/')
        pyperclip.copy(p4_place)
    else:
        tkinter.messagebox.showinfo('提示', '不属于p4路径')


def del_file_path(messages, arg):
    file_name = messages[arg]['file_name']
    xmltool = XmlTool()
    xmltool.del_message(file_name)


def set_file_path(arg, var_usr_name, var_usr_pwd):
    # label
    change_file_name.clear()
    messages = xmltool.read_message()
    var_usr_name.set(messages[arg]['file_name'])
    var_usr_pwd.set(messages[arg]['file_path'])
    change_file_name.append(arg)
    change_file_name.append(messages[arg]['file_name'])

def change_file_path(top, var_usr_name, var_usr_pwd):
    if change_file_name:
        file_name = to_save(top, var_usr_name, var_usr_pwd, change_file_path=change_file_name[1])
        label_list[change_file_name[0]]['text'] = file_name
        tkinter.messagebox.showinfo('提示', '修改成功')
        change_file_name.clear()
    else:
        tkinter.messagebox.showinfo('提示','请点击设置后修改')



def to_save(top, file_name, file_path, change_file_path=None):
        messageDict = {}
        messages = xmltool.read_message()
        usr_name = file_name.get()
        usr_pwd = file_path.get()
        if len(usr_name)>=10:
            tkinter.messagebox.showinfo('提示', '标签名过长')
            return False
        if usr_pwd and usr_name:
            messageDict['file_name'] = str(usr_name)
            messageDict['file_path'] = str(usr_pwd)
            if not os.path.exists(usr_pwd):
                tkinter.messagebox.showinfo('提示', '本地路径不存在')
                return False
            if change_file_path:
                xmltool.change_message(messageDict, change_file_path)
                return messageDict['file_name']
            else:
                if messages:
                    for message in messages:
                        if messageDict['file_name'] == message['file_name'] or messageDict['file_path'] == message['file_path']:
                            tkinter.messagebox.showinfo('提示', '已存在该标签名或路径')
                            return False
                xmltool.add_message(messageDict)
                show_add_message(top, messageDict, file_name, file_path)
            tkinter.messagebox.showinfo('提示', '保存成功')
            change_file_name.clear()
        else:
            tkinter.messagebox.showinfo('提示','标签名称和路径不能为空')

    # top.quit()
    # time.sleep(10)
    # show_message()
    # top.update()
def to_clear(file_name, file_path):
    file_name.delete(0, 'end')
    file_path.delete(0, 'end')
    change_file_name.clear()

def show_add_message(top, messageDict, usr_name, usr_pwd):
    messages = xmltool.read_message()
    num = len(messages) - 1
    label = tkinter.Label(top, text=messageDict['file_name'], bg="pink")
    label_list.append(label)
    btn_login1 = tkinter.Button(top, text="打开", command=lambda arg=num: open_file(arg))
    btn_login2 = tkinter.Button(top, text="复制", command=lambda arg=num: copy_file_path(arg))
    btn_login3 = tkinter.Button(top, text="p4", command=lambda arg=num: copy_file_path_p4(arg))
    btn_login4 = tkinter.Button(top, text="设置", command=lambda arg=num: set_file_path(arg, usr_name, usr_pwd))
    label.grid(column=0, row=num)
    btn_login1.grid(row=num, column=1)
    btn_login2.grid(row=num, column=2)
    btn_login3.grid(row=num, column=3)
    btn_login4.grid(row=num, column=4)





def show_message():
    top = tkinter.Tk()
    top.title("自定义文件夹")
    top.geometry('550x700')
    messages = xmltool.read_message()
    tkinter.Label(top, text='标签名:   (不超过10个字)', font=('Arial', 14)).place(x=265, y=15)
    tkinter.Label(top, text='完整路径:', font=('Arial', 14)).place(x=265, y=75)

    # 用户名
    var_usr_name = tkinter.StringVar()
    # var_usr_name.set('任意输入关键字')
    entry_usr_name = tkinter.Entry(top, textvariable=var_usr_name, font=('Arial', 14))
    entry_usr_name.place(x=270, y=45)
    # 用户密码
    var_usr_pwd = tkinter.StringVar()
    # var_usr_pwd.set("输入正确地址")
    entry_usr_pwd = tkinter.Entry(top, textvariable=var_usr_pwd, font=('Arial', 14))
    entry_usr_pwd.place(x=270, y=105)
    btn_login = tkinter.Button(top, text='保存', command=lambda: to_save(top, var_usr_name, var_usr_pwd))
    btn_login3 = tkinter.Button(top, text='清空', command=lambda: to_clear(entry_usr_name, entry_usr_pwd))
    btn_login2 = tkinter.Button(top, text='修改', command=lambda: change_file_path(top, entry_usr_name, entry_usr_pwd))
    btn_login.place(x=413, y=135)
    btn_login3.place(x=313, y=135)
    btn_login2.place(x=363, y=135)

    if messages:
        i = 0
        for message in messages:
            label = tkinter.Label(top, text=message['file_name'], bg="pink")
            label_list.append(label)
            btn_login1 = tkinter.Button(top, text="打开", command=lambda arg=i:open_file(arg))
            btn_login2 = tkinter.Button(top, text="复制", command=lambda arg=i:copy_file_path(arg))
            btn_login3 = tkinter.Button(top, text="p4", command=lambda arg=i:copy_file_path_p4(arg))
            btn_login4 = tkinter.Button(top, text="设置", command=lambda arg=i:set_file_path(arg, var_usr_name, var_usr_pwd))
            label.grid(column=0, row=i)
            btn_login1.grid(row=i, column=1)
            btn_login2.grid(row=i, column=2)
            btn_login3.grid(row=i, column=3)
            btn_login4.grid(row=i, column=4)
            i+=1
            # print(label.grid_info())
            # print(btn_login1.grid_info())
            # print(btn_login2.grid_info())
        # 第5步，用户信息

    top.mainloop()


show_message()