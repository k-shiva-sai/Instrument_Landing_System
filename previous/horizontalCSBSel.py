from tkinter import *
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
imFrame.place(x=-580,y=-650)
antennaFrame = Frame(height=680,width=50)
antennaFrame.place(x=0,y=140)
top = Frame(bg="#9C4242",height=35,width=1200)
top.pack(side=TOP,fill=X)
controlPanel = Frame(bg="#3A3939",height=680,width=300)
controlPanel.pack(side=RIGHT,fill=X)
controlPanel.pack_propagate(0)
controlPanel.grid_propagate(0)
top.pack_propagate(0)
controlPanelTitle = Label(controlPanel,text="Control Panel",fg="white",bg="#3A3939",font=("Ubuntu",18,"bold"))
controlPanelTitle.pack(side=TOP,padx=10,pady=10)


def plotRadiation(theta,E):
  for w in imFrame.winfo_children():
    w.destroy()
  fig = plt.Figure(figsize=(20,20))
  ax=fig.add_axes([0.1,0.1,0.8,0.8],polar=True)
  ax.set_xticks(np.arange(-np.pi,np.pi,np.pi/90))
  ax.set_thetamin(90)
  ax.set_thetamax(-90)
  ax.plot(theta,E)
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
  newWindow.geometry("600x150")
  Label(newWindow,text="Antennas",bg="#3A3939",fg="white").grid(row=0,column=0)
  Label(newWindow,text="Distance",bg="#3A3939",fg="white").grid(row=1,column=0)
  Label(newWindow,text="Amplitude",bg="#3A3939",fg="white").grid(row=2,column=0)
  Label(newWindow,text="Phase",bg="#3A3939",fg="white").grid(row=3,column=0)
  for i in range(7):
    Label(newWindow,text="A"+str(i+1),bg="#3A3939",fg="white").grid(row=0,column=i+1)
  for i in range(3):
    for j in  range(7):
      Entry(newWindow,textvariable=rightVars[i][j],width=8,bg="#4a4848",fg="white",insertbackground="white").grid(row=i+1,column=j+1)

#control panel
isOn = True
dArr = [0.95,3.04,5.30,7.73,10.34,13.13,16.09,19.23,22.54,26.03]
#16.09,22.54,26.03

def labelWidgets(root,labelList):
  for i in range(len(labelList)):
    Label(root,text=labelList[i],bg="#3A3939",fg="white",font=("Ubuntu",15)).grid(row=i+1,padx=20,pady=10)

def fTheta(t):
  return pow(10,-(0.0000442*pow(abs(t),3)+0.0023678*pow(abs(t),2)+0.016252*abs(t))/20)

def Generate():
  global isOn
  par = int(length_input.get())
  ph = int(phase_input.get())
  ph = np.radians(ph)
  theta = np.arange(-np.pi/4, np.pi/4, 0.005)
  #if isOn else 2*np.sin(-np.pi/2+par*np.pi*np.sin(theta+ph)/2)
  E=0*theta
  for i in range(7):
    if antennaIsOn[7+i]:
      E += 2*float(rightVars[1][i].get())*(np.cos((2/2.72)*float(rightVars[0][i].get())*np.pi*np.sin(theta)))*fTheta(theta)
  #f(o) phi amp
  plotRadiation(theta,E)
  
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

antennaIsOn = [True for _ in range(14)]
lDefaultValues = [[0.818,2.862,4.906,6.95,8.994,11.038,13.082],
[0.9432,1,0.6746,0.4270,0.1616,0.046,0],
[0,0,0,0,0,0,0,0,0,0]]
rDefaultValues = [[0.818,2.862,4.906,6.95,8.994,11.038,13.082],
[0.9432,1,0.6746,0.4270,0.1616,0.046,0],
[0,0,0,00,0,0,0,0,0]]
leftVars = [[0 for i in range(7)] for _ in range(3)]
rightVars = [[0 for i in range(7)] for _ in range(3)]
for i in range(3):
  for j in range(7):
    leftVars[i][j] = StringVar(value=lDefaultValues[i][j])
    rightVars[i][j] = StringVar(value=rDefaultValues[i][j])
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
    if antennaIsOn[i]:
        antennas.append(Button(antennaFrame,image=antennaOnImage,bd=0,command=lambda c = i: antennaCommand(c)))
    else:
        antennas.append(Button(antennaFrame,image=antennaOffImage,bd=0,command=lambda c = i: antennaCommand(c)))
    antennas[i].pack(side=TOP)

switch = Button(controlPanel,image=rightSwitch,bd=0,highlightthickness=0,relief=SUNKEN,padx=0,pady=0,bg="#3A3939",command=buttonPressed)
switch.grid(row=1,column=1)
Label(controlPanel, text="Out Phase",bg="#3A3939",fg="white").grid(row=1,column=0,sticky='e')
Label(controlPanel, text="In Phase",bg="#3A3939",fg="white").grid(row=1,column=2)
Label(controlPanel, text="D",font=("Ubuntu",15),width=12,bg="#3A3939",fg="white").grid(row=2, column=0)

length_input = Scale(controlPanel, from_=0.2, to=5,resolution=0.1,orient=HORIZONTAL,length= 100,bg="#3A3939",fg='white')

length_input.grid(row = 2, column = 1,pady=10)

Label(controlPanel, text="Phase",font=("Ubuntu",15),width=12,bg="#3A3939",fg="white").grid(row=3, column=0)

phase_input = Scale(controlPanel, from_=0, to=360,resolution=0.1,orient=HORIZONTAL,length= 100,bg="#3A3939",fg='white')

phase_input.grid(row = 3, column = 1,pady=10)
param_button = Button(controlPanel,text = "Adjust antenna \n parameters",padx=8,pady=6,cursor='hand2', relief=FLAT,
  command=openParametersWindow).grid(row=4,column=1,pady=10)
submit_button = Button(controlPanel,text = "Generate",padx=8,pady=6,cursor='hand2', relief=FLAT,
  command=lambda: Generate()).grid(row=5,column=1)

root.mainloop()