from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox as tmsg
from pytube import YouTube
root = Tk()

check = False
defaultPath = "C:/Users/Lenovo/Desktop/Coding/Tkinter/chat-gpt"

# All Logic
# Add path where to stored download
def addPath():
    # Geometry and title
    newWindow = Toplevel(root)
    newWindow.geometry("600x700")
    newWindow.title("YouTube Downloader Tool")

    # width,height
    newWindow.minsize(300,300)

    # width,height
    newWindow.maxsize(300,300)

    newWindow.wm_iconbitmap("youtube.ico")

    # Add path Gui
    global pathValue
    pathLabel = Label(newWindow, text="Add Path").pack(padx=10,pady=4)
    pathValue = StringVar()
    with open("path.txt", "r") as f:       
        data = f.read()
        if(len(data)>0):
            pathValue.set(data)
    pathEntry = Entry(newWindow, textvariable=pathValue).pack(pady=2)
    addBtn = Button(newWindow, text="Add", command=Add).pack(pady=2)

# adding path to a path.txt 
def Add(): 
    f = open("path.txt", "w")
    f.write(pathValue.get())
    f.close()
    tmsg.showinfo("Added", "Your path is Added")

# About of this project
def about():
    tmsg.showinfo("About", """This is a youtube video Downloader in which you can download video. You can download one video at one time. You can't download age-restriction video.""")

# Choose in which format object will downlaod(audio or video, both(Video))
def Format():
    global check
    if(len(urlVar.get())>0):
        if(len(var_type.get())>0):         
            statusvar.set("Waiting...")
            sbar.update() 
            link = urlVar.get()
            try:
                youtube = YouTube(link)
            except:
                tmsg.showinfo("Error!", "Somethings wrong maybe you entered wrong url or internet issue.")
                statusvar.set("Ready")
            else:
                global title
                global videos
                global yt_length
                title = youtube.title 
                yt_length = str(youtube.length) 

                if(var_type.get()=="Audio"):
                    lbx.delete(0, END)
                    try:
                        videos = youtube.streams.filter(only_audio=True)
                    except:
                        tmsg.showinfo("Error!", "This video can't be download because of age restricted in thsi video.")
                        statusvar.set("Ready")
                    else:                       
                        check = True
                        vid = list(enumerate(videos))
                        for i in vid:                       
                            lbx.insert(ACTIVE, i)

                elif(var_type.get()=="Video"):
                    lbx.delete(0, END)
                    try:
                        videos = youtube.streams.filter(only_video=True)
                    except:                      
                        tmsg.showinfo("Error!", "This video can't be download because of age restricted in thsi video.")
                        statusvar.set("Ready")
                    else:                      
                        check = True
                        vid = list(enumerate(videos))
                        for i in vid:                        
                            lbx.insert(ACTIVE, i)

                else:
                    lbx.delete(0, END)
                    try:
                        videos = youtube.streams.filter(progressive=True)
                    except:                      
                        tmsg.showinfo("Error!", "This video can't be download because of age restriction in this video.")
                        statusvar.set("Ready")
                    else:
                        check = True
                        vid = list(enumerate(videos))
                        for i in vid:                         
                            lbx.insert(ACTIVE, i)
               
                if(check==True):                 
                    typebar.set("(Title): "+title+" "+" \n("+yt_length+" seconds)")    
                    type_video.pack(pady=15, anchor=CENTER)
                    lbx.pack(fill=X)
                    download.pack(pady=8,anchor=CENTER)
                    downloadEntry.pack(anchor=CENTER)
                    dPath.pack(pady=4,anchor=CENTER)
                    downloadBtn.pack(pady=2,anchor=CENTER)
                    statusvar.set("Ready")

# Downloading Function
def downloading():
    val = downloadVar.get()
    if(len(val)>0):
        val = int(val)
        statusvar.set("downloading...")
        sbar.update()   

        try:
            if(dVar.get()==0):
                try:   
                    with open("path.txt", "r") as f:
                        data = f.read()
                        if(len(data)>0):
                            videos[val].download(data) 
                        else:
                            videos[val].download(defaultPath) 
                except:
                    videos[val].download(defaultPath) 
            elif(dVar.get()==1):
                videos[val].download(defaultPath)   
        except:
            tmsg.showinfo("Error", "Somethings wrong maybe you entered wrong No.(integer) or internet issue.")
            statusvar.set("Ready")
        else:              
            statusvar.set("Ready")
            tmsg.showinfo("Download", "Your content is downloaded")


# Geometry and title
root.geometry("600x700")
root.title("YouTube Downloader Tool")

# width,height
root.minsize(600,700)

# width,height
root.maxsize(600,700)

root.wm_iconbitmap("youtube.ico")

# Menus and submenu
mainmenu = Menu(root)
m1 = Menu(mainmenu, tearoff=0)
m1.add_command(label="Add download path", command=addPath)
root.config(menu=mainmenu)
mainmenu.add_cascade(label='File', menu=m1)

mainmenu.add_command(label="About", command=about)
root.config(menu=mainmenu)

mainmenu.add_command(label="Exit", command=quit)
root.config(menu=mainmenu)

# Url of Youtube Video
url = Label(root, text="Enter Url").pack(pady=4,anchor=CENTER)
urlVar = StringVar()
urlEntry = Entry(root, textvariable=urlVar).pack(anchor=CENTER)

# show audio or video 
var_type = StringVar()
radio = Radiobutton(root, text="Audio(Only)",  variable=var_type, value="Audio").pack(pady=4)
radio = Radiobutton(root, text="Video(Only)", variable=var_type, value="Video").pack()
radio = Radiobutton(root, text="Video(Both)",  variable=var_type, value="VideoB").pack(padx=8,pady=3)
urlBtn =  Button(root, text="Choose Format", command=Format).pack(pady=2,anchor=CENTER)

# Type of video label
typebar = StringVar()
type_video = Label(root, textvariable=typebar)
lbx = Listbox(root)

# input in (int) for downloading
download = Label(root, text="Enter No.")
downloadVar = StringVar()
downloadEntry = Entry(root, textvariable=downloadVar)
dVar = IntVar()
dPath = Checkbutton(text="Want to download in default path ?", variable = dVar)
downloadBtn =  Button(root, text="download", command=downloading)


# Status Bar
statusvar = StringVar()
statusvar.set("Ready")
sbar = Label(root, textvariable=statusvar, relief=SUNKEN, anchor="w")
sbar.pack(side=BOTTOM, fill=X)

# Note for users
note = Label(root, text=''' Note: \n 1. If you have to downlaod content then you have to choose number(integer) eg-1,2,3,0 then it will downloaded. \n
 2. If you provide path then content will saved on your given specific path rather than default path(if you checked). \n
 3. If you don't provide path then content will saved in default location(if not checked).''').pack(side=BOTTOM, pady=30)

root.mainloop()