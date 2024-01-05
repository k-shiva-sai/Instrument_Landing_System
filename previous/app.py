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

def sinSignal(amp,freq,samples,samplingFrequency,phase):
  return amp * np.sin(phase+2*np.pi*freq*samples/samplingFrequency)

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
    Fc = float(var["Fc (MHz)"].get())*10**6
    Fm1 = float(var["Fm1"].get())
    Fm2 = float(var["Fm2"].get())
    Am = float(var["Am"].get())
    Am1 = float(var["Am1"].get())
    Am2 = float(var["Am2"].get())
    m1 = float(var["m1"].get())
    m2 = float(var["m2"].get())
    duration = float(var["time (sec)"].get())
    pc1 = float(var["pc1"].get())
    pc2 = float(var["pc2"].get())
    ps1 = float(var["ps1"].get())
    ps2 = float(var["ps2"].get())
    print(ps1,ps2)

    samplingFrequency = Fc*10
    samples = np.arange(samplingFrequency*duration)
    m90c = sinSignal(Am1,Fm1,samples,samplingFrequency,np.radians(pc1))
    m150c = sinSignal(Am2,Fm2,samples,samplingFrequency,np.radians(pc2))
    m90s = sinSignal(Am1,Fm1,samples,samplingFrequency,np.radians(ps1))
    m150s = sinSignal(Am2,Fm2,samples,samplingFrequency,np.radians(ps2))
    carrier = sinSignal(1,Fc,samples,samplingFrequency,0)
    csb = Am*(1 + m1*m90c + m2*m150c)*carrier
    sbo = Am*(m2*m150s + m1*m90s)*carrier
    plot(samples,samplingFrequency,sbo,csb)
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
labelList = ["Fc (MHz)","Fm1","Fm2","Am","Am1","Am2","m1","m2","time (sec)","pc1","pc2","ps1","ps2"]
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