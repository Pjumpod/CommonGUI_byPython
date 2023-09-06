import logging
import threading
import time
from datetime import date
from datetime import datetime
import tkinter as tk
import re
import socket
import os
from subprocess import Popen, PIPE, STDOUT
import glob
from PIL import Image, ImageTk

def text_update(std_input=""):
    t1.insert("end", std_input + '\n\r')
    t1.update()
    t1.see("end")

def clear():
    #t1.delete("1.0", tk.END)
    entry1.delete(0, tk.END)
    #entry2.delete(0, tk.END)
    entry3.delete(0, tk.END)

def findLatestImage(path):
    list_of_files = glob.glob(path + "\\temp\\cos_scope_image\\*.png")
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def checkPassFail(strResult):
    strResult.lower()
    # TODO capture the final result from str.
    return True

def runTest():
    entry1.configure(state="disabled")
    entry3.configure(state="disabled")
    # TODO change the picture files and customer script.
    camera_pic = r"C:\tmp\APD_1000101040_20230410_145200.png"
    close_lid_pic = r"C:\tmp\APD_1000101040_20230410_145200.png"
    customer_script = r"D:\Project\python\main.py"

    t1.delete("1.0", tk.END)
    test_operator = entry1.get()
    test_station_location = entry2.get()
    device_serial = entry3.get()

    t1.configure(background="lightyellow")

    test_time_start = datetime.now().strftime("%H:%M:%S")
    test_date = date.today().strftime('%Y_%m_%d')
    starttime = time.time()
    starttime_tag = datetime.now().strftime("%Y%m%d%H%M%S")

    text_update('EN: ' + test_operator)
    text_update('Machine No.: ' + test_station_location)
    text_update('LCOS SN: ' + device_serial)
    text_update('Date: ' + test_date + " " + test_time_start)
    text_update("Testing................................")

    t = 0
    if str(c.get()) == "pre-burn":
        t = 0

    if str(c.get()) == "post-burn":
        t = 1

    if str(c.get()) == "all":
        t = 2

    line = ""
    text_update("path = " + str(os.path.dirname(os.path.abspath(customer_script))))
    with Popen(['python', '-u', customer_script], stdin=PIPE, stdout=PIPE,
                universal_newlines=True, bufsize=1, cwd=os.path.dirname(os.path.abspath(customer_script))) as cat:
        while cat.poll() is None:
            if "Press enter to move to camera location" in line:
                a = tk.Tk()
                a.geometry('+0+0')
                a.title("Warning!!")
                p = tk.PhotoImage(master=a, file=camera_pic)  # insert image
                tk.Label(master=a, image=p).pack()
                tk.Label(master=a, text="Press enter to move to camera location.", font=("Helvetica", 18)).pack()
                tk.Button(master=a, text="Enter", font=("Helvetica", 16), command=a.withdraw).pack()
                text_update("A stat => " + str(a.state()).lower())
                # noinspection PyBroadException
                try:
                    while str(a.state()).lower() != "withdrawn":
                            # it needs to have text to prevent the thread hang.
                        text_update("wait for prompt")
                        time.sleep(0.1)
                except Exception:
                    pass
                print("", file=cat.stdin, flush=True)
                line += cat.stdout.readline()
                text_update("-> " + line)
                line = ""
            if "Press enter when lid is closed" in line:
                a = tk.Tk()
                a.geometry('+0+0')
                a.title("Warning!!")
                p = tk.PhotoImage(master=a, file=close_lid_pic)  # insert image
                tk.Label(master=a, image=p).pack()
                tk.Label(master=a, text="Press enter when lid is closed.", font=("Helvetica", 18)).pack()
                tk.Button(master=a, text="Enter", font=("Helvetica", 16), command=a.withdraw).pack()
                text_update("A stat => " + str(a.state()).lower())
                # noinspection PyBroadException
                try:
                    while str(a.state()).lower() != "withdrawn":
                        # it needs to have text to prevent the thread hang.
                        text_update("wait for prompt")
                        time.sleep(0.1)
                except Exception:
                    pass
                print("", file=cat.stdin, flush=True)
                line += cat.stdout.readline()
                text_update("-> " + line)
                line = ""
            if "Enter SN" in line:
                print(device_serial, file=cat.stdin, flush=True)
                line += cat.stdout.readline()
                text_update("-> " + line)
                line = ""
            if "For all other tests" in line:
                print(t, file=cat.stdin, flush=True)
                line += cat.stdout.readline()
                text_update("-> " + line)
                line = ""
            if ("Press ctrl + C" in line) | ("I told you" in line):
                cat.kill()
                break
            tmp = cat.stdout.read(1)
            line += str(tmp)
            if tmp == "\n":
                text_update("-> " + line)
                line = ""

    duration = time.time() - starttime
    text_update('Duration: ' + str(duration))

    logfilename = device_serial + "_" + starttime_tag + ".txt"
    outputTexts = t1.get("1.0", "end")
    with open(os.path.join(logpath, logfilename), "w") as f:
        f.write(outputTexts)
    final_result = checkPassFail(outputTexts)
    latestImage = findLatestImage(os.path.dirname(os.path.abspath(customer_script)))
    osc_image = Image.open(latestImage)
    osc_image = osc_image.resize((400, 300), Image.LANCZOS)
    osc_image = ImageTk.PhotoImage(osc_image)
    if device_serial in latestImage:
        # TODO remove this text_update line.
        text_update("latestImage = " + latestImage)
        pictureBox.configure(image=osc_image)
        pictureBox.image = osc_image
        # replace the box at same position.
        pictureBox.place(x=60, y=240, width=400, height=300)
    result_color = ["light salmon", "lightgreen"][final_result]
    t1.configure(background=result_color)
    entry1.configure(background="white")
    entry3.configure(background="white")
    entry1.configure(state="normal")
    entry3.configure(state="normal")
    text_update("Result is " + str(final_result))
    return

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

    sn_barcode = entry3.get().upper()
    if not re.match('^[A-Z]{2}\d{6}$', sn_barcode):
        sn = tk.Tk()
        sn.title("Wrong!!")
        entry3.configure(background="OrangeRed")
        tk.Label(master=sn, text="SN is incorrect format!!!. Please try again", font=("Helvetica", 18)).pack()
        entry3.delete(0, tk.END)
        return
    runTest()
    text_update("DONE TEST")
    return

def destroyForm():
    logging.critical("windows exit")
    window.quit()
    window.destroy()

if __name__ == '__main__':
    window = tk.Tk()
    window.title("LCOS Test")
    window.geometry("1200x550+50+50")
    window.protocol('WM_DELETE_WINDOW', destroyForm)

    #TODO change the path of blank.png
    pictureBlank = r"D:\Project\python\blank.png"

    logpath=r"C:\tmp" #save log file
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

    SN = tk.Label(master=window,text="Substrate SN:", font=("Helvetica",18))
    SN.place(x=0,y=90)
    entry3 = tk.Entry(master=window,font=("Times",12))
    entry3.place(x=160,y=90,width=280,height=30)
    entry3.configure(background="white")

    test = tk.Label(master=window,text="Test Number:", font=("Helvetica",18))
    test.place(x=0,y=130)
    test_number = ["pre-burn","post-burn","all"]
    c = tk.StringVar(master=window)
    c.set( "all" )
    drop = tk.OptionMenu(window,c,*test_number)
    drop.place(x=160,y=130)

    t1 = tk.Text(master=window)
    t1.pack(side=tk.RIGHT,fill = tk.Y,expand=True)
    t1.place(x=480, y=10, width=700, height=530)

    runBtn = tk.Button(master=window,text="RUN!",font=("Helvetica",16),command=checkInput)
    runBtn.place(x=180,y=190,width=100,height=30)
    clear = tk.Button(master=window,text="Clear",font=("Helvetica",16),command=clear)
    clear.place(x=60,y=190,width=100,height=30)

    img_init = tk.PhotoImage(file=pictureBlank)
    pictureBox = tk.Label(master=window, image=img_init)
    pictureBox.place(x=60,y=240,width=400,height=300)

    window.mainloop()


