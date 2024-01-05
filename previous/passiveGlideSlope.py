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

def plot(vi,Ldiff):
  for w in imFrame.winfo_children():
    w.destroy()
  fig = plt.Figure(dpi=125)
  pltSbo = fig.add_subplot(111,title="Frensels kirchoffs diffraction",xlabel="Vi",ylabel="Ldiff")
  fig.tight_layout()
  pltSbo.grid()
  # pltSbo.set_yticks(np.arange(-25,6,5))
  # pltSbo.set_xticks(np.arange(-5,5.1,1))
  pltSbo.plot(vi,Ldiff)
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

# 1. calculate 1st frensels zone radius
# 2. calculate clearance
# 3. cal knife edge prop factor Vi
#  i. cal normalize electric field
#  ii. cal path loss Ldiff
# 4. plot Ldiff vs Vi

def cal_Loss(vi):
    if vi < -1:
        return 0
    elif vi<=0:
        return 20*np.log10(0.5 - 0.62*vi)
    elif vi<=1:
        return 20*np.log10(0.5*np.exp(-0.95*vi))
    elif vi<=2.4:
        return 20*np.log10(0.4 - np.sqrt(0.1184-(0.38-0.1*vi)**2))
    else:
        return 20*np.log10(0.225/vi)


def Generate(var):
    Fc = float(var["Fc (MHz)"].get())*10**6
    D = float(var["D"].get())
    Ht = float(var["Ht"].get())
    Hr = float(var["Hr"].get())
    hobs = float(var["Hobs"].get())
    lamda = (3*(10**8))/Fc
    ang = np.arctan((Ht+Hr)/D)
    print(np.rad2deg(ang))
    Xo = D/(2 + D*ang/lamda)
    L = 2*Xo - (D/2)*((2 - 3**0.5)/(2+0.338*D*ang))
    W = (4.44/(1/D + 0.169*ang**2))**0.5
    print("Xo: {0:.3f} L: {1:.3f} W: {2:.3f} ".format(Xo,L,W))

    #plot(vi,20*np.log10(F))

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
labelList = ["Fc (MHz)","D","Ht","Hr","Hobs"]
defaultValues = [330,10000,3,200,0]
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