from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image,ImageTk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)

def donothing():
  pass

root = Tk()
root.geometry("1200x680")
root.title("ILS Simulator")
root.iconphoto(False,PhotoImage(file="assets/flight.png"))
top = Frame(bg="#9C4242",height=35,width=1200)
imFrame = Frame(height=645,width=900)
imFrame.place(x=0,y=35)
top.pack(side=TOP,fill=X)
controlPanel = Frame(bg="#3A3939",height=680,width=300)
controlPanel.pack(side=RIGHT,fill=X)
controlPanel.pack_propagate(0)
controlPanel.grid_propagate(0)
top.pack_propagate(0)
controlPanelTitle = Label(controlPanel,text="Control Panel",fg="white",bg="#3A3939",font=("Ubuntu",18,"bold"))
controlPanelTitle.pack(side=TOP,padx=10,pady=10)

def sinSignal(amp,freq,samples,samplesPerSecond,phase):
  return amp * np.sin(phase+2*np.pi*freq*samples/samplesPerSecond)

def plot(samples,sps,sbo,csb):
  for w in imFrame.winfo_children():
    w.destroy()
  fig = plt.Figure(dpi=125)
  pltSbo = fig.add_subplot(311,title="SBO")
  pltCsb = fig.add_subplot(312,title="CSB",ylabel="Amplitude (volts)")
  pltGuide = fig.add_subplot(313,title="Guindace Signal",xlabel="time (sec)")
  fig.tight_layout()
  pltSbo.plot(samples/sps,sbo)
  pltCsb.plot(samples/sps,csb)
  pltGuide.plot(samples/sps,sbo+csb)
  # fig.savefig('out.jpg')
  # canvas = Canvas(imFrame,width=999,height=999)
  # canvas.pack()
  # pilImage = Image.open("out.jpg")
  # image = ImageTk.PhotoImage(pilImage)
  # canvas.create_image(400,400,image=image)
  canvas = FigureCanvasTkAgg(fig,imFrame)
  canvas.draw()
  wid = canvas.get_tk_widget()
  wid.place(x=0,y=0)
  toolbar = NavigationToolbar2Tk(canvas,imFrame)
  toolbar.update()
  tool = canvas.get_tk_widget()
  tool.pack(side=BOTTOM)

def Generate(var):
    obsDistance = float(var[labelList[0]].get())
    obsAngleWrtRunway = float(var[labelList[1]].get())
    obsHeight = float(var[labelList[2]].get())
    obsAngle = np.degrees(np.arctan(obsHeight/obsDistance))
    if(obsAngleWrtRunway<=10 and obsAngle>=0.75):
        print("Obstacle will effect Lz1")
    else:
        print("Obstacle won't effect Lz1")

    if(obsAngleWrtRunway<=35 and obsAngleWrtRunway>10 and obsAngle>=1.1):
        print("Obstacle will effect Lz2")
    else:
        print("Obstacle won't effect Lz2")

    if(obsAngleWrtRunway<=8 and obsAngle>=1.1):
        print("Obstacle will effect GS")
    else:
        print("Obstacle won't effect GS")    
    #plot(samples,samplesPerSecond,sbo,csb)
    # print(sys.getrefcount(csb))

#menu bar
menuFontStyle = ('Roboto',10,'bold')
file = Label(top,text="File",bg="#9C4242",fg="white",font=menuFontStyle)
file.pack(side=LEFT,padx=6,pady=2)
menu = Label(top,text="Menu",bg="#9C4242",fg="white",font=menuFontStyle)
menu.pack(side=LEFT,padx=6,pady=2)
help = Label(top,text="Help",bg="#9C4242",fg="white",font=menuFontStyle)
help.pack(side=LEFT,padx=6,pady=2)

#control panel
def labelWidgets(root,labelList):
  for i in range(len(labelList)):
    Label(root,text=labelList[i],bg="#3A3939",fg="white",font=("Ubuntu",15)).grid(row=i+1,padx=20,pady=6)

controlPanel.grid_rowconfigure(0,minsize=50)
labelList = ["Obs Distance","angle wrt Runway","Obs Height"]
defaultValues = [0.0003,3,5,1,1,1,0.4,0.4,1,0,0,0,0]
labelWidgets(controlPanel,labelList)
var = {}
for i in range(len(labelList)):
  var[labelList[i]] = StringVar(value=defaultValues[i])

for i in range(len(labelList)):
  Entry(controlPanel,textvariable=var[labelList[i]],font=("Ubuntu",12),width=12,
  bg="#4a4848",fg="white",insertbackground="white").grid(row=i+1,column=1,padx=20,pady=6)

submit_button = Button(controlPanel,text = "Generate",padx=8,pady=4,cursor='hand2', relief=FLAT,
  command=lambda: Generate(var)).grid(row=14,column=1)

root.mainloop()