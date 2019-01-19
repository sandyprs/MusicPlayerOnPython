from tkinter import*
import time
from ttkthemes import themed_tk as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import threading
import os
from pygame import mixer
from mutagen.mp3 import MP3
#==========================def==================
index1 = 0
index2 = 0
songlst = []
st="welcome to my music player"
def choosedir():
    global file,playing,paused,songlst,lst,index1
    playing = True
    paused = False

    file = filedialog.askopenfilename()

    #play()
    songlst.append(file)
    lst.insert(index1,os.path.basename(file))
    index1+=1

def dlt():
    song_no = lst.curselection()
    song_no = int(song_no[0])
    song_name = songlst[song_no]
    selected = song_name
    select = song_no
    lst.delete(select)
    songlst.remove(selected)

def msg():
    stop()
    messagebox.askyesno("confirm","do you really want to exit?")
    root.destroy()

#========================================layout========================
root= tk.ThemedTk()
root.get_themes()                 # Returns a list of all themes that can be set
root.set_theme("clearlooks")
root.geometry("600x500+300+300")
root.resizable(width=False,height=False)
root.title("music player")
root.iconbitmap(default=r"C:\Users\SANJIB\PycharmProjects\1st\musiciicon.ico")
mixer.init()

menu=Menu(root,bg="grey",relief=RAISED)
root.config(menu=menu)
submenu=Menu(menu)
menu.add_cascade(menu=submenu,label="open")
submenu.add_command(label="FILE",command=choosedir)
submenu.add_command(label="EXIT",command=msg)


nm="                make some noise!!"

name=Label(root,text="MUSIC PLAYER",bg="green",fg="red",font="bold")
name.pack(fill=X)



song=Label(root,text=nm,bg="gold",font="bold",anchor=W)
song.pack(fill=X)



lstfrm=Frame(root)
lstfrm.pack()
lst=Listbox(lstfrm,width=50,bd=5)
lst.pack(side=LEFT)

addbtn=ttk.Button(lstfrm,text="add",command=choosedir)
addbtn.pack(side=LEFT,anchor=N,padx=5)
dltbtn=ttk.Button(lstfrm,text="delete",command=dlt)
dltbtn.pack(side=TOP,anchor=S,padx=5)



#============================def===========================

def time_dtl(t_time):
    global paused,c_time,index2
    c_time = t_time
    while c_time and mixer.music.get_busy():
        if paused:
            continue
        else:
            c_time = c_time-1
            #print(c_time)
            time.sleep(1)
            mins, secs = divmod(c_time, 60)
            mins = round(mins)
            secs = round(secs)
            c_frmt = "{:02d}:{:02d}".format(mins, secs)
            c_tm_lbl["text"] = c_frmt
            if c_time==0:
                next()


def tot_time(index2):
    song_name = songlst[index2]
    audio = MP3(song_name)
    t_time = audio.info.length
    return t_time,song_name

def timing_lab(t_time):
    mins, secs = divmod(t_time, 60)
    mins = round(mins)
    secs = round(secs)
    t_frmt = "{:02d}:{:02d}".format(mins, secs)
    t_tm_lbl["text"] = t_frmt


def play():
    global index2,playing,paused,songlst,lst,nm,song_name,th1


    if playing:
        if paused:
            mixer.music.unpause()
            stsbar["text"] = "playing"
            pl["image"]=psim
            playing=False
            paused = False
            return
        try:
            song_no = lst.curselection()
            song_no = int(song_no[0])
            index2=song_no
            t_time,song_name=tot_time(index2)
            timing_lab(t_time)

            nm = "playing.. " + os.path.basename(song_name)
            song["text"]=nm
            mixer.music.load(song_name)
            mixer.music.play()
            th1=threading.Thread(target=time_dtl,args=(t_time,))
            th1.start()
            pl["image"] = psim
            stsbar["text"]="playing"

            playing=False
        except:
            messagebox.showinfo("Recheck", "choose file first")
    else:
        paused=True
        pl["image"] = plim
        mixer.music.pause()
        stsbar["text"] = "paused"
        playing=True


def next():
    global index2,song_name,nm,songlst,lst,c_time,th1
    #stop()
    #th1.terminate()
    c_time=0
    index2 += 1
    try:
        t_time, song_name = tot_time(index2)
        timing_lab(t_time)

        mixer.music.load(songlst[index2])
        mixer.music.play()
        th1 = threading.Thread(target=time_dtl, args=(t_time,))
        th1.start()
        pl["image"] = psim
        stsbar["text"] = "next"
        song_name = songlst[index2]
        nm = "playing.. " + os.path.basename(song_name)
        song["text"] = nm
    except:
        t_tm_lbl["text"] = "--:--"
        c_tm_lbl["text"] = "--:--"
        stop()

def prev():
    global index2,song_name,nm,songlst,c_time
    #stop()
    c_time = 0
    index2 -= 1
    try:
        t_time, song_name = tot_time(index2)
        timing_lab(t_time)
        mixer.music.load(songlst[index2])
        mixer.music.play()
        th1 = threading.Thread(target=time_dtl, args=(t_time,))
        th1.start()
        pl["image"] = psim
        stsbar["text"] = "previous"
        song_name=songlst[index2]
        nm = "playing.. " + os.path.basename(song_name)
        song["text"] = nm
    except:
        t_tm_lbl["text"] = "--:--"
        c_tm_lbl["text"] = "--:--"
        stop()


def stop():
    global playing,paused
    mixer.music.stop()
    stsbar["text"] = "stopped"
    pl["image"] = plim
    playing = True
    paused = False


def ch_vol(volume):
    vol=float(volume)
    #vol=int(volume)/100
    mixer.music.set_volume(vol)


muted=False
def mute():
    global muted
    if muted:

        scl.set(50)
        mixer.music.set_volume(50)
        volbtn.config(image=volim1)
        muted = False

    else:

        scl.set(0)
        mixer.music.set_volume(0)
        volbtn.config(image=volim2)
        muted = True


#=======================btn===============

preim=PhotoImage(file="control-first-128.png")
nxtim=PhotoImage(file=r"C:\Users\SANJIB\PycharmProjects\1st\control-last-128.png")
stpim=PhotoImage(file=r"C:\Users\SANJIB\PycharmProjects\1st\control-stop-128.png")
plim=PhotoImage(file=r"C:\Users\SANJIB\PycharmProjects\1st\play.png")
volim1=PhotoImage(file=r"C:\Users\SANJIB\PycharmProjects\1st\sound.png")
volim2=PhotoImage(file=r"C:\Users\SANJIB\PycharmProjects\1st\novol.png")
psim=PhotoImage(file=r"C:\Users\SANJIB\PycharmProjects\1st\pause_button-128.png")
#======================================================================================

timefrm=Frame(root,width=100)
timefrm.pack(side=TOP,pady=10)

c_tm_lbl=Label(timefrm,text="--:--")
c_tm_lbl.grid(row=0,column=0,padx=40)

t_tm_lbl=Label(timefrm,text="--:--")
t_tm_lbl.grid(row=0,column=1,padx=250)


butfrm=Frame(root)
butfrm.pack()
pre=Button(butfrm,image=preim,height=75,width=100,relief=RAISED,bg="dark grey",bd=3,command=prev)
pre.pack(side=LEFT,padx=5,pady=10)

pl=Button(butfrm,image=plim,height=75,width=100,relief=RAISED,bg="dark grey",bd=3,command=play)
pl.pack(side=LEFT,padx=5,pady=10)

nxt=Button(butfrm,image=nxtim,height=75,width=100,relief=RAISED,bg="dark grey",bd=3,command=next)
nxt.pack(side=LEFT,padx=5,pady=10)

stp=Button(butfrm,image=stpim,height=75,width=100,relief=RAISED,bg="dark grey",bd=3,command=stop)
stp.pack(side=LEFT,padx=5,pady=10)

#=================================================================================

sclfrm=Frame(root)
sclfrm.pack()

volbtn=ttk.Button(sclfrm,image=volim1,command=mute)
volbtn.pack(side=LEFT)

scl=ttk.Scale(sclfrm,orient=HORIZONTAL,command=ch_vol)
scl.pack(side=LEFT,padx=7)
scl.set(0.5)
mixer.music.set_volume(0.5)


stsbar=Label(root,text=st,bg="grey",height=2,anchor=W)
stsbar.pack(side=BOTTOM,fill=X)


root.protocol("WM_DELETE_WINDOW",msg)
root.mainloop()