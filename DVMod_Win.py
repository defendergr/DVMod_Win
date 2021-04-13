import tkinter as tk
import tkinter.ttk as ttk
from tkinter import simpledialog
import os
import requests
import threading
import shutil
import json
import urllib.request
import subprocess
# ------------------------------MS imports for admin privileges start---------------------------------------------------
import ctypes
import enum
import sys
# ------------------------------MS imports for admin privileges end-----------------------------------------------------

class App():
    def __init__(self, root):
        #ri8misis - 8esh para8iroy
        self.root = root
        root.title("Defender's Video Mod for Kodi")
        root.resizable(False,False)
        self.widgets()
        win_width = root.winfo_reqwidth()
        win_hight = root.winfo_reqheight()
        pos_right = int(root.winfo_screenwidth()/3 - win_width/3)
        pos_down = int(root.winfo_screenheight()/3 - win_hight/3)
        root.geometry("800x450+{}+{}".format(pos_right, pos_down))
        root.iconbitmap("icon.ico")
        self.ZIP_URL = 'http://defendergr.000webhostapp.com/DVMod.zip'
        self.ZIP_UPDATE_URL = 'http://defendergr.000webhostapp.com/DVModUpdate.zip'
        self.ZIP_EXTRACT_FOLDER = os.path.join(os.environ['APPDATA'], "Kodi")
        self.ZIP_FILENAME = 'DVMod.zip'
        self.ZIP_UPDATE_FILENAME = 'DVModUpdate.zip'

    def main_text(self):
        self.CHECK = os.path.isfile('dvm.ver')
        self.lfile = 'dvm.ver'
        self.ver_check = float(json.load(urllib.request.urlopen('http://defendergr.000webhostapp.com/dvm.ver')))
        try:
            self.localver = float(open(self.lfile, 'r').read().strip())
            self.remotever = self.ver_check
        except:
            self.localver = 0
            self.remotever = self.ver_check
        if self.localver == self.remotever:
            self.canvas.itemconfig(self.pos_text, text=f'Το DVMod είναι στην τελευτέα έκδοση {self.localver}')
            self.canvas.delete(self.pos_pg_bar)
            self.button1['text'] = 'Άνοιγμα'
        elif self.CHECK == True and self.localver < self.remotever:
            self.canvas.itemconfig(self.pos_text, text=f'Υπάρχει μια νέα αναβάθμιση του DVMod\nΈκδοση {self.remotever}')
            self.button1['text'] = 'Αναβάθμιση'
        else:
            self.canvas.itemconfig(self.pos_text, text=f'Λήψη και εγκατάσταση του DVMod\nΈκδοση {self.remotever}')

    def widgets(self):
        #basiko para8iro
        self.text = ''
        self.bt_text = 'OK'
        self.font = 'Arial 15 bold'
        self.frame = tk.Frame(self.root)
        self.frame.pack(expand=1, fill='both')
        self.canvas = tk.Canvas(self.frame, bg='lightblue')
        self.canvas.pack(expand=1, fill='both')
        #dimiourgia antikimenon ston camva
        self.image_bg = tk.PhotoImage(file='image.gif')
        self.canvas.create_image(0, 0, image=self.image_bg, anchor='nw')
        self.pg_bar = ttk.Progressbar(self.canvas, orient = 'horizontal', length = 500, mode = 'determinate')
        self.pg_bar.pack()
        self.button1 = tk.Button(self.canvas, text=self.bt_text, font='Arial 12', command=self.start, width=15, anchor='s')
        self.button1.pack()
        self.button2 = tk.Button(self.canvas, text='Έξοδος', font='Arial 12', command=self.root.destroy, width=10, anchor='s')
        self.button2.pack()
        self.buttoni = tk.Button(self.canvas, text='About', font='Arial 8 bold', width=6, command=self.info, anchor='s')
        self.buttoni.pack()
        #topothetish antikimenon ston camva
        self.pos_text = self.canvas.create_text(400, 180, text=self.text, font=self.font, width=400, anchor='n', fill='white')
        self.pos_pg_bar = self.canvas.create_window(400, 250, anchor='s', window=self.pg_bar)
        self.pos_b1 = self.canvas.create_window(400,300, anchor='s', window=self.button1)
        self.pos_b2 = self.canvas.create_window(750, 400, anchor='se', window=self.button2)
        self.pos_bi = self.canvas.create_window(797, 3, anchor='ne', window=self.buttoni)
        self.main_text()

    def refresh(self):
        self.root.update()
        self.root.after(1000, self.refresh)

    def start(self):
        self.refresh()
        self.th = threading.Thread(target=self.download_content, daemon = True)
        self.th.start()

    def info(self):
        simpledialog.messagebox.showinfo('About', 'DVMod Launcher Version 1.6\nCredits: \nΚωνσταντίνος Καρακασίδης')

    def download_file(self, url):
        local_filename = url.split('/')[-1]
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    try:
                        lf = os.path.getsize(local_filename)
                        lfs = (lf / 1024)/1024
                        rfs = (int(r.headers['Content-length'])/1024)/1024
                        self.pg_bar['value'] = ((lf / int(r.headers['Content-length']))*100)+1
                        self.per = int(self.pg_bar['value'])
                        self.canvas.itemconfig(self.pos_text, text=f'Λήψη του DVMod {int(lfs)}MB από {int(rfs)}MB {self.per}%\nΈκδοση {self.remotever}')
                        print(int(self.pg_bar['value']))
                        f.write(chunk)
                    except ZeroDivisionError:
                        self.pg_bar['value'] = 0
        with open('dvm.ver', 'w') as f:
            for i in str(self.ver_check):
                f.write(i)
                print(i)

    def download_content(self):
        if self.localver == self.remotever:
            self.button1['state'] = 'disabled'
            self.button1['text'] = 'Φώρτοση...'
            self.open_kodi()
        elif self.CHECK== True:
            self.button1['state'] = 'disabled'
            self.button1['text'] = 'Αναβαθμίζεται...'
            self.download_file(self.ZIP_UPDATE_URL)
            shutil.unpack_archive(self.ZIP_UPDATE_FILENAME, self.ZIP_EXTRACT_FOLDER)
            self.canvas.itemconfig(self.pos_text, text='Η αναβάθμιση ολοκληρώθηκε με επιτυχία')
            self.open_kodi()
        else:
            self.button1['state'] = 'disabled'
            self.button1['text'] = 'Λήψη...'
            self.download_file(self.ZIP_URL)
            self.button1['text'] = 'Εγκατάσταση...'
            self.canvas.itemconfig(self.pos_text, text='Γίνεται εγκατάσταση\nπαρακαλώ περιμενετε...')
            shutil.unpack_archive(self.ZIP_FILENAME, self.ZIP_EXTRACT_FOLDER)
            self.canvas.itemconfig(self.pos_text, text='Η εγκατάσταση ολοκληρώθηκε με επιτυχία')
            self.button1['text'] = 'Φώρτοση...'
            self.open_kodi()

    def open_kodi(self):
        self.button1['text'] = 'Φώρτοση...'
        prf = os.environ["ProgramFiles"]
        subprocess.call(f'"{prf}'+'\Kodi\kodi.exe"')
        # os.startfile(f'"{prf}'+'\Kodi\kodi.exe"')
        # os.system(f'"{prf}'+'\Kodi\kodi.exe"')
        self.root.destroy()





# ------------------------------MS code for admin privileges start------------------------------------------------------
class SW(enum.IntEnum):

    HIDE = 0
    MAXIMIZE = 3
    MINIMIZE = 6
    RESTORE = 9
    SHOW = 5
    SHOWDEFAULT = 10
    SHOWMAXIMIZED = 3
    SHOWMINIMIZED = 2
    SHOWMINNOACTIVE = 7
    SHOWNA = 8
    SHOWNOACTIVATE = 4
    SHOWNORMAL = 1


class ERROR(enum.IntEnum):

    ZERO = 0
    FILE_NOT_FOUND = 2
    PATH_NOT_FOUND = 3
    BAD_FORMAT = 11
    ACCESS_DENIED = 5
    ASSOC_INCOMPLETE = 27
    DDE_BUSY = 30
    DDE_FAIL = 29
    DDE_TIMEOUT = 28
    DLL_NOT_FOUND = 32
    NO_ASSOC = 31
    OOM = 8
    SHARE = 26


def bootstrap():
    if ctypes.windll.shell32.IsUserAnAdmin():
        root = tk.Tk()#apo edo ksekinaei to programa mou
        App(root)#apo edo ksekinaei to programa mou
        root.mainloop()#apo edo ksekinaei to programa mou
    else:
        hinstance = ctypes.windll.shell32.ShellExecuteW(
            None, 'runas', sys.executable, sys.argv[0], None, SW.SHOWNORMAL
        )
        if hinstance <= 32:
            raise RuntimeError(ERROR(hinstance))

# ------------------------------MS code for admin privileges end--------------------------------------------------------

if __name__ == '__main__':
    app = bootstrap()
