from tkinter import *
from turtle import color
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image,ImageTk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from numpy.lib.shape_base import expand_dims

def donothing():
  pass

root = Tk()
root.geometry("1200x680")
root.title("ILS Simulator")
root.iconphoto(False,PhotoImage(file="assets/flight.png"))
imFrame = Frame(height=680,width=900)
imFrame.place(x=50,y=35)
antennaFrame = Frame(height=680,width=50)
antennaFrame.place(x=0,y=35)
top = Frame(bg="#9C4242",height=35,width=1200)
top.pack(side=TOP,fill=X)
controlPanel = Frame(bg="#3A3939",height=680,width=300)
controlPanel.pack(side=RIGHT,fill=X)
controlPanel.pack_propagate(0)
controlPanel.grid_propagate(0)
top.pack_propagate(0)
controlPanelTitle = Label(controlPanel,text="Control Panel",fg="white",bg="#3A3939",font=("Ubuntu",18,"bold"))
controlPanelTitle.pack(side=TOP,padx=10,pady=10)


def plotRadiation(theta,Ecsb,Esbo):
  for w in imFrame.winfo_children():
    w.destroy()
  fig = plt.Figure(figsize=(20,20))
  ax=fig.add_axes([0.1,0.1,0.8,0.8],polar=True)
  ax.set_xticks(np.arange(-np.pi,np.pi,np.pi/90))
  ax.set_thetamin(90)
  ax.set_thetamax(-90)
  ax.plot(theta,Ecsb)
  ax.plot(theta,18*Esbo)
  canvas = FigureCanvasTkAgg(fig,imFrame)
  canvas.draw()
  wid = canvas.get_tk_widget()
  wid.place(x=0,y=0)
  toolbar = NavigationToolbar2Tk(canvas,imFrame)
  toolbar.update()
  tool = canvas.get_tk_widget()
  tool.pack(side=RIGHT)

def plotDdmMonitoring(theta,Ecsb,Esbo,Ddm):
  theta = np.rad2deg(theta)
  for w in imFrame.winfo_children():
    w.destroy()
  fig = plt.Figure(dpi=125)
  pltCsb = fig.add_subplot(311,title="CSB")
  pltSbo = fig.add_subplot(312,title="SBO")
  pltGuide = fig.add_subplot(313,title="DDM",xlabel="theta")
  fig.tight_layout()
  pltCsb.plot(theta,Ecsb)
  pltSbo.plot(theta,Esbo)
  pltGuide.plot(theta,Ddm)
  canvas = FigureCanvasTkAgg(fig,imFrame)
  canvas.draw()
  wid = canvas.get_tk_widget()
  wid.place(x=0,y=0)
  toolbar = NavigationToolbar2Tk(canvas,imFrame)
  toolbar.update()
  tool = canvas.get_tk_widget()
  tool.pack(side=RIGHT)

#menu bar
menuFontStyle = ('Roboto',10,'bold')
file = Label(top,text="File",bg="#9C4242",fg="white",font=menuFontStyle)
file.pack(side=LEFT,padx=6,pady=2)
menu = Label(top,text="Menu",bg="#9C4242",fg="white",font=menuFontStyle)
menu.pack(side=LEFT,padx=6,pady=2)
help = Label(top,text="Help",bg="#9C4242",fg="white",font=menuFontStyle)
help.pack(side=LEFT,padx=6,pady=2)

#antenna parameters window
def openParametersWindow():
  newWindow = Toplevel(root,bg="#3A3939")
  newWindow.title("Localizer antenna parameters")
  newWindow.geometry("600x300")
  newWindow.grid_rowconfigure(10,minsize=50)
  Label(newWindow,text="CSB",bg="#3A3939",fg="white").grid(row=0,column=0)
  Label(newWindow,text="Distance",bg="#3A3939",fg="white").grid(row=1,column=0)
  Label(newWindow,text="Amplitude",bg="#3A3939",fg="white").grid(row=2,column=0)
  Label(newWindow,text="Phase",bg="#3A3939",fg="white").grid(row=3,column=0)
  for i in range(10):
    Label(newWindow,text="A"+str(i+1),bg="#3A3939",fg="white").grid(row=0,column=i+1)
  for i in range(3):
    for j in  range(10):
      Entry(newWindow,textvariable=rightVars[i][j],width=8,bg="#4a4848",fg="white",insertbackground="white").grid(row=i+1,column=j+1)

  Label(newWindow,text="SBO",bg="#3A3939",fg="white").grid(row=10+2,column=0)
  Label(newWindow,text="Distance",bg="#3A3939",fg="white").grid(row=11+2,column=0)
  Label(newWindow,text="Amplitude",bg="#3A3939",fg="white").grid(row=12+2,column=0)
  Label(newWindow,text="Phase",bg="#3A3939",fg="white").grid(row=13+2,column=0)
  for i in range(10):
    Label(newWindow,text="A"+str(i+1),bg="#3A3939",fg="white").grid(row=10+2,column=i+1)
  for i in range(3):
    for j in  range(10):
      Entry(newWindow,textvariable=rSboVars[i][j],width=8,bg="#4a4848",fg="white",insertbackground="white").grid(row=i+11+2,column=j+1)


#control panel
isOn = True
#16.09,22.54,26.03

def labelWidgets(root,labelList):
  for i in range(len(labelList)):
    Label(root,text=labelList[i],bg="#3A3939",fg="white",font=("Ubuntu",15)).grid(row=i+1,padx=20,pady=10)

def fTheta(t):
  return pow(10,-(0.0000442*pow(abs(t),3)+0.0023678*pow(abs(t),2)+0.0162524*abs(t))/20)

def cal_Ddm(th):
  Ec,Es = 0,0
  for i in range(10):
    if antennaIsOn[10+i]:
        Ec+=2*float(rightVars[1][i].get())*(
          np.cos((2/2.72)*float(rightVars[0][i].get())*np.pi*np.sin(th)))
  for i in range(10):
    if antennaIsOn[10+i]:
        Es += 2*float(rSboVars[1][i].get())*(
            (np.sin((2/2.72)*float(rightVars[0][i].get())*np.pi*np.sin(th))))
  Ec = abs(Ec)
  Es = abs(Es)
  return [2*Es/Ec,Ec,Es]

def Generate():
  global isOn
  # par = int(length_input.get())
  # ph = int(phase_input.get())
  # ph = np.radians(ph)
  theta = np.arange(0, np.deg2rad(3)+0.0001, 0.005)
  #if isOn else 2*np.sin(-np.pi/2+par*np.pi*np.sin(theta+ph)/2)
  Ecsb=0*theta
  Esbo=0*theta
  # Fc = 0j*theta
  # Fs = 0j*theta
  # Rp,Th,Phi = 7000,2,0
  # Pl,Pu = 2*np.pi*90, 2*np.pi*180
  # Wo = 2*np.pi*(110000000)
  # Ec,Es=0,0
  th = np.arctan(105/4000)
  for i in range(10):
    if antennaIsOn[10+i]:
        Ecsb += 2*float(rightVars[1][i].get())*(np.cos((2/2.72)*float(rightVars[0][i].get())*np.pi*np.sin(theta)))
        Esbo += 2*float(rSboVars[1][i].get())*(np.sin((2/2.72)*float(rSboVars[0][i].get())*np.pi*np.sin(theta)))

def ddmMonitor():
  limit = float(var[labelList[0]].get())
  sectorWidth = float(var[labelList[1]].get())
  reqDdm = float(var[labelList[2]].get())
  curDdm = float(var[labelList[3]].get())
  afCsb = float(var[labelList[4]].get())
  afSbo = float(var[labelList[5]].get())
  reqAfSbo = float(var[labelList[6]].get())
  theta = np.arange(0, np.deg2rad(limit)+0.0001, 0.005)

  Ecsb=0*theta
  Esbo=0*theta
  ang = np.deg2rad(sectorWidth/2)
  for i in range(10):
    if antennaIsOn[10+i]:
        Ecsb += 2*float(rightVars[1][i].get())*(np.cos((2/2.72)*
        float(rightVars[0][i].get())*np.pi*np.sin(theta)))
        Esbo += 2*float(rSboVars[1][i].get())*(np.sin((2/2.72)*
        float(rSboVars[0][i].get())*np.pi*np.sin(theta)))
  ddmRes = cal_Ddm(ang)
  var[labelList[3]].set(round(ddmRes[0],3))
  var[labelList[4]].set(round(ddmRes[1],3))
  var[labelList[5]].set(round(ddmRes[2],3))
  var[labelList[6]].set(round(reqDdm*ddmRes[1]/2,3))
  # for i in np.arange(0,20,0.01):
  #   d = cal_Ddm(np.deg2rad(i))
  #   if d<0.1559 and d>0.15499:
  #     print(i,d)
  #     break

  ddm = 2*Esbo/Ecsb

  Ecsb = abs(Ecsb)
  Esbo = abs(Esbo)
  #f(o) phi amp
  plotDdmMonitoring(theta,Ecsb,Esbo,ddm)
  
def buttonPressed():
  global isOn
  if isOn:
    switch.config(image=leftSwitch)
  else:
    switch.config(image=rightSwitch)
  isOn = not isOn

controlPanel.grid_rowconfigure(0,minsize=50)
leftSwitch = PhotoImage(file='assets/offState.png')
rightSwitch = PhotoImage(file='assets/onState.png')
antennaOnImage = PhotoImage(file="assets/antenna_on.png")
antennaOffImage = PhotoImage(file="assets/antenna_off.png")

antennaIsOn = [True for _ in range(20)]

lDefaultValues = [[0.95,3.04,5.30,7.73,10.34,13.13,16.09,19.23,22.54,26.03],
[93,100,100,93,82,66,45,29,15,11],
[0,0,0,0,0,0,0,0,0,0]]
rDefaultValues = [[1.19,3.04,5.30,7.73,10.34,13.13,16.09,19.23,22.54,26.03],
[93,100,100,93,82,66,45,29,15,11],
[0,0,0,0,0,0,0,0,0,0]]
rDefaultValuesSBO = [[1.19,3.04,5.30,7.73,10.34,13.13,16.09,19.23,22.54,26.03],
[0.55,1.89,3.38,4.82,6,6.66,6.59,5.75,4.2,3.29],
[0,0,0,0,0,0,0,0,0,0]]
leftVars = [[0 for i in range(10)] for _ in range(3)]
rightVars = [[0 for i in range(10)] for _ in range(3)]
rSboVars = [[0 for i in range(10)] for _ in range(3)]

# rDefaultValues = [[1.90,9.54,15.82,21.8,27.8,33.8,16.09,19.23,22.54,26.03],
# [100,54.9,33.5,19,8.1,2.4,45,29,15,11],
# [0,0,0,0,0,0,0,0,0,0]]
# rDefaultValuesSBO = [[1.90,9.54,15.82,21.8,27.8,33.8,16.09,19.23,22.54,26.03],
# [7.1,5,6.72,4.88,2.61,0.9,6.59,5.75,4.2,3.29],
# [0,0,0,0,0,0,0,0,0,0]]

# for i in range(4):
#   antennaIsOn[i] = False
#   antennaIsOn[19-i] = False

for i in range(3):
  for j in range(10):
    leftVars[i][j] = StringVar(value=lDefaultValues[i][j])
    rightVars[i][j] = StringVar(value=rDefaultValues[i][j])
    rSboVars[i][j] = StringVar(value=rDefaultValuesSBO[i][j])
antennas = []

def antennaCommand(i):
  j = len(antennaIsOn)-i-1
  if antennaIsOn[i]:
    antennas[i].config(image=antennaOffImage)
    antennas[j].config(image=antennaOffImage)
  else:
    antennas[i].config(image=antennaOnImage)
    antennas[j].config(image=antennaOnImage)
  antennaIsOn[i] = not antennaIsOn[i]
  antennaIsOn[j] = not antennaIsOn[j]

for i in range(len(antennaIsOn)):
  im = antennaOnImage if antennaIsOn[i] else antennaOffImage
  antennas.append(Button(antennaFrame,image=im,bd=0,command=lambda c = i: antennaCommand(c)))
  antennas[i].pack(side=TOP)

switch = Button(controlPanel,image=rightSwitch,bd=0,highlightthickness=0,relief=SUNKEN,padx=0,pady=0,bg="#3A3939",command=buttonPressed)
# switch.grid(row=1,column=1)
# Label(controlPanel, text="Out Phase",bg="#3A3939",fg="white").grid(row=1,column=0,sticky='e')
# Label(controlPanel, text="In Phase",bg="#3A3939",fg="white").grid(row=1,column=2)
# Label(controlPanel, text="D",font=("Ubuntu",15),width=12,bg="#3A3939",fg="white").grid(row=2, column=0)

def labelWidgets(root,labelList):
  for i in range(len(labelList)):
    Label(root,text=labelList[i],bg="#3A3939",fg="white",font=("Ubuntu",15)).grid(row=i+1,padx=20,pady=6)

controlPanel.grid_rowconfigure(0,minsize=50)
labelList = ["Theta range","sector width","req DDM","cur DDM","AF CSB","AF SBO","Req AF SBO"]
defaultValues = [10,2,0.155,0,0,0,0,0]
labelWidgets(controlPanel,labelList)
var = {}
for i in range(len(labelList)):
  var[labelList[i]] = StringVar(value=defaultValues[i])

for i in range(len(labelList)):
  Entry(controlPanel,textvariable=var[labelList[i]],font=("Ubuntu",12),width=12,
  bg="#4a4848",fg="white",insertbackground="white").grid(row=i+1,column=1,padx=20,pady=6)

# length_input = Scale(controlPanel, from_=0.2, to=5,resolution=0.1,orient=HORIZONTAL,length= 100,bg="#3A3939",fg='white')

# length_input.grid(row = 2, column = 1,pady=10)

# Label(controlPanel, text="Phase",font=("Ubuntu",15),width=12,bg="#3A3939",fg="white").grid(row=3, column=0)

# phase_input = Scale(controlPanel, from_=0, to=360,resolution=0.1,orient=HORIZONTAL,length= 100,bg="#3A3939",fg='white')

# phase_input.grid(row = 3, column = 1,pady=10)
param_button = Button(controlPanel,text = "Adjust antenna \n parameters",padx=8,pady=6,cursor='hand2', relief=FLAT,
  command=openParametersWindow).grid(row=len(labelList)+1,column=1,pady=10)
submit_button = Button(controlPanel,text = "Generate",padx=8,pady=6,cursor='hand2', relief=FLAT,
  command=lambda: ddmMonitor()).grid(row=len(labelList)+2,column=1)

root.mainloop()