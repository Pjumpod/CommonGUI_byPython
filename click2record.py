import logging
import threading
import time
from datetime import date
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
import re
import socket
import os
import glob
import pandas as pd
import openpyxl
# from subprocess import Popen, PIPE, STDOUT
# from PIL import Image, ImageTk

def clear():
    #t1.delete("1.0", tk.END)
    entry1.delete(0, tk.END)
    #entry2.delete(0, tk.END)
    entry3.delete(0, tk.END)

def chooseDir():
    backup_path = entry6.get()
    entry6.delete(0,tk.END)
    save_path_browse =  filedialog.askdirectory(parent=window, initialdir=backup_path, title='Please select a directory')
    if save_path_browse != "":
        entry6.insert("end",save_path_browse)
    else:
        entry6.insert("end",backup_path)

def runTest():
    entry1.configure(state="disabled")
    entry3.configure(state="disabled")
    entry4.configure(state="disabled")
    entry5.configure(state="disabled")
    entry6.configure(state="disabled")
    path_to_save = entry6.get()
    file_to_save = os.path.join(path_to_save,"record.xlsx")
    df = pd.DataFrame(columns=['#','SerialNumber', 'Datetime', 'Machine','EN','APD','Value'])
    en_record = [entry1.get()]
    sn_record = [entry3.get()]
    machine_record = [entry2.get()]
    apd_record = [entry4.get()]
    value_record = [entry5.get()]
    time_record = [datetime.now().strftime("%Y/%m/%d %H:%M:%S")]
    data={'SerialNumber':sn_record, 'Datetime':time_record, 'Machine':machine_record,
                            'EN':en_record,'APD':apd_record, 'Value':value_record}
    df=pd.DataFrame(data)
    df.to_excel(file_to_save)
    entry1.configure(state="normal")
    entry3.configure(state="normal")
    entry4.configure(state="normal")
    entry5.configure(state="normal")
    entry6.configure(state="normal")
    return True

def checkInput():
    
    if len(entry1.get()) != 6:
        enno = tk.Tk()
        enno.title("Wrong!!")
        entry1.configure(background="OrangeRed")
        tk.Label(master=enno,text="Operator EN is incorrect!!!. Please try again", font=("Helvetica",18)).pack()
        entry1.delete(0, tk.END)
        return

    if not entry1.get().isnumeric():
        enno = tk.Tk()
        enno.title("Wrong!!")
        entry1.configure(background="OrangeRed")
        tk.Label(master=enno,text="Operator EN is incorrect!!!. Please try again", font=("Helvetica",18)).pack()
        entry1.delete(0, tk.END)
        return
    else:
        entry1.configure(background="LightGreen")

    sn_barcode = entry3.get().upper()
    # if not re.match('^[A-Z]{2}\d{6}$', sn_barcode):
    if len(sn_barcode) < 1:
        sn_error = tk.Tk()
        sn_error.title("Wrong!!")
        entry3.configure(background="OrangeRed")
        tk.Label(master=sn_error, text="SN is incorrect format!!!. Please try again", font=("Helvetica", 18)).pack()
        entry3.delete(0, tk.END)
        return
    else:
        entry3.configure(background="LightGreen")
    
    path_to_save = entry6.get()
    if len(path_to_save) < 3:
        path_error = tk.Tk()
        path_error.title("Wrong!!")
        entry6.configure(background="OrangeRed")
        tk.Label(master=path_error,text="PATH is not correct!!. Please try again", font=("Helvetica",18)).pack()
        entry6.delete(0, tk.END)
        return
    
    if os.path.exists(path_to_save) == False:
        path_error = tk.Tk()
        path_error.title("Wrong!!")
        entry6.configure(background="OrangeRed")
        tk.Label(master=path_error,text="PATH " + path_to_save + " is not exist!!. Please try again", font=("Helvetica",18)).pack()
        entry6.delete(0, tk.END)
        return
    else:
        entry6.configure(background="LightGreen")
    
    result = runTest()
    success_error = tk.Tk()
    if result:
        success_error.title("Log file SAVE!!")
        tk.Label(master=success_error,text="Logfile success recorded", font=("Helvetica",18)).pack()
    else:
        success_error.title("Log file cannot SAVE!!")
        tk.Label(master=success_error,text="Logfile failed to record", font=("Helvetica",18)).pack()
    entry1.configure(background="white")
    entry3.configure(background="white")
    entry6.configure(background="white")
    return

def destroyForm():
    logging.critical("windows exit")
    window.quit()
    window.destroy()

if __name__ == '__main__':
    window = tk.Tk()
    window.title("Click2Save Test")
    window.geometry("600x350+50+50")
    window.protocol('WM_DELETE_WINDOW', destroyForm)

    logpath=r"C:\tmp" #save log file
    save_log_path = r"C:\tmp"
    isExist = os.path.exists(logpath)
    if not isExist:
        os.makedirs(path)

    en = tk.Label(master=window,text="EN:", font=("Helvetica",18))
    en.place(x=110,y=10)
    entry1 = tk.Entry(master=window,font=("Times",12))
    entry1.place(x=160,y=10,width=280,height=30)
    entry1.configure(background="white")

    machine = tk.Label(master=window,text="Machine No.:", font=("Helvetica",18))
    machine.place(x=8,y=50)
    entry2 = tk.Entry(master=window,font=("Times",12))
    entry2.place(x=160,y=50,width=280,height=30)
    entry2.insert("end",socket.gethostname())
    entry2.configure(state="disabled")

    SN = tk.Label(master=window,text="SN :", font=("Helvetica",18))
    SN.place(x=105,y=90)
    entry3 = tk.Entry(master=window,font=("Times",12))
    entry3.place(x=160,y=90,width=280,height=30)
    entry3.configure(background="white")
    
    APD = tk.Label(master=window,text="APD :", font=("Helvetica",18))
    APD.place(x=90,y=130)
    entry4 = tk.Entry(master=window,font=("Times",12))
    entry4.place(x=160,y=130,width=280,height=30)
    entry4.configure(background="white")
    
    value = tk.Label(master=window,text="VALUE :", font=("Helvetica",18))
    value.place(x=60,y=170)
    entry5 = tk.Entry(master=window,font=("Times",12))
    entry5.place(x=160,y=170,width=280,height=30)
    entry5.configure(background="white")
    
    b_chooseDir = tk.Button(window, text = "Chose Folder", width = 20, height = 3, command = chooseDir)
    b_chooseDir.place(x = 450,y = 200)
    b_chooseDir.width = 100
    save_path = tk.Label(master=window,text="SAVE PATH :", font=("Helvetica",18))
    save_path.place(x=0,y=210)
    entry6 = tk.Entry(master=window,font=("Times",12))
    entry6.place(x=160,y=210,width=280,height=30)
    entry6.configure(background="white")
    entry6.insert("end",save_log_path)

    # test = tk.Label(master=window,text="Test Number:", font=("Helvetica",18))
    # test.place(x=0,y=130)
    # test_number = ["pre-burn","post-burn","all"]
    # c = tk.StringVar(master=window)
    # c.set( "all" )
    # drop = tk.OptionMenu(window,c,*test_number)
    # drop.place(x=160,y=130)

    # t1 = tk.Text(master=window)
    # t1.pack(side=tk.RIGHT,fill = tk.Y,expand=True)
    # t1.place(x=480, y=10, width=700, height=530)

    runBtn = tk.Button(master=window,text="RUN!",font=("Helvetica",16),command=checkInput)
    runBtn.place(x=180,y=270,width=100,height=30)
    clear = tk.Button(master=window,text="Clear",font=("Helvetica",16),command=clear)
    clear.place(x=60,y=270,width=100,height=30)

    # img_init = tk.PhotoImage(file=pictureBlank)
    # pictureBox = tk.Label(master=window, image=img_init)
    # pictureBox.place(x=60,y=240,width=400,height=300)

    window.mainloop()
