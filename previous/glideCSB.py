from tkinter import *
import matplotlib.pyplot as plt
import numpy
from numpy import (sin,cos,tan,pi,arange,rad2deg,deg2rad,radians)
from PIL import Image,ImageTk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)

def donothing():
  pass

root = Tk()
root.geometry("1200x680")
root.title("ILS Simulator")
root.iconphoto(False,PhotoImage(file="assets/flight.png"))
imFrame = Frame(height=680,width=900)
imFrame.place(x=-600,y=-700)
top = Frame(bg="#9C4242",height=35,width=1200)
top.pack(side=TOP,fill=X)
controlPanel = Frame(bg="#3A3939",height=680,width=300)
controlPanel.pack(side=RIGHT,fill=X)
controlPanel.pack_propagate(0)
controlPanel.grid_propagate(0)
top.pack_propagate(0)
controlPanelTitle = Label(controlPanel,text="Control Panel",fg="white",bg="#3A3939",font=("Ubuntu",18,"bold"))
controlPanelTitle.pack(side=TOP,padx=10,pady=10)


def plotRadiation(theta,E,F):
  for w in imFrame.winfo_children():
    w.destroy()
  fig = plt.Figure(figsize=(20,20))
  ax=fig.add_axes([0.1,0.1,0.8,0.8],polar=True)
  ax.set_xticks(arange(-pi,pi,pi/60))
  ax.set_thetamin(90)
  ax.set_thetamax(-90)
  ax.set_rlabel_position(0)
  ax.plot(theta,E)
  ax.plot(theta,F)
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

#control panel
isOn = True

def labelWidgets(root,labelList):
  for i in range(len(labelList)):
    Label(root,text=labelList[i],bg="#3A3939",fg="white",font=("Ubuntu",15)).grid(row=i+1,padx=20,pady=10)

def fTheta(t):
  return pow(10,-(0.0000442*pow(abs(t),3)+0.0023678*pow(abs(t),2)+0.016252*abs(t))/20)

def Generate():
  global isOn
  par = int(length_input.get())
  ph = int(phase_input.get())
  ph = radians(ph)
  theta = arange(0, pi/4, 0.001)
  #E = 2*sin((2/2.72)*1.56*pi*sin(theta+ph)) if isOn else 2*sin(-pi/2+par*pi*sin(theta+ph)/2)
  E = None
  t = sin(deg2rad(3))
  phi = (pi/2)*(sin(theta/t))
  k = 0.117
  Ecm = -0.5*sin(pi*sin(theta)/t)*2
  Ecu = sin(1.5*pi*sin(theta)/t)*2
  Esl = -0.5*sin(0.5*pi*sin(theta)/t)*2
  Esm = 1*sin(pi*sin(theta)/t)*2
  Esu = -0.5*sin(1.5*pi*sin(theta)/t)*2
  lower = Esl 
  middle = Ecm + Esm
  upper = Ecu + Esu
  Ecsb = 2*(sin(0.5*pi*sin(theta)/t)-0.5*sin(pi*sin(theta)/t))
  Esbo = 2*(-0.5*sin(0.5*pi*sin(theta)/t)+1*sin(pi*sin(theta)/t)-0.5*sin(1.5*pi*sin(theta)/t))
  Fcsb = sin(phi*(cos(phi)-1))
  Fsbo = (0.5*sin(phi)-sin(2*phi)+0.5*sin(3*phi))
  # if isOn:
  #   E = sin(phi*(cos(phi)-1))
  # else:
  #   E = k*(0.5*sin(phi)-sin(2*phi)+0.5*sin(3*phi))
  Fcsb = abs(Fcsb)
  Fsbo = abs(Fsbo)
  plt.figure()
  ax1 = plt.subplot(111)
  ax1.plot(theta,abs(Esl),'r')
  ax1.plot(theta,abs(Esm),'g')
  ax1.plot(theta,abs(Esu),'b')
  plt.show()
  # ax1.plot(theta,abs(lower),'r')
  # ax1.plot(theta,abs(middle),'g')
  # ax1.plot(theta,abs(upper),'b')
  ax2 = plt.subplot(111, projection='polar')
  ax2.plot(theta,abs(lower),'r')
  ax2.plot(theta,abs(middle),'g')
  ax2.plot(theta,abs(upper),'b')
  plt.show()
  ddm = 4*0.117*cos((pi/2)*sin(theta)/t)
  plt.figure()
  plt.plot(rad2deg(theta),ddm)
  plt.grid()
  plt.xticks(arange(0, 12, step=1))
  #plt.yticks(arange(-0.5, 0.5, step=0.05))
  plt.show()

  plotRadiation(theta,abs(Ecsb),abs(Esbo))

#k=0.117
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


switch = Button(controlPanel,image=rightSwitch,bd=0,highlightthickness=0,relief=SUNKEN,padx=0,pady=0,bg="#3A3939",command=buttonPressed)
switch.grid(row=1,column=1)
Label(controlPanel, text="Out Phase",bg="#3A3939",fg="white").grid(row=1,column=0,sticky='e')
Label(controlPanel, text="In Phase",bg="#3A3939",fg="white").grid(row=1,column=2)
Label(controlPanel, text="D",font=("Ubuntu",15),width=12,bg="#3A3939",fg="white").grid(row=2, column=0)

length_input = Scale(controlPanel, from_=0, to=10,resolution=1,orient=HORIZONTAL,length= 100,bg="#3A3939",fg='white')

length_input.grid(row = 2, column = 1,pady=10)

Label(controlPanel, text="Phase",font=("Ubuntu",15),width=12,bg="#3A3939",fg="white").grid(row=3, column=0)

phase_input = Scale(controlPanel, from_=0, to=360,resolution=0.1,orient=HORIZONTAL,length= 100,bg="#3A3939",fg='white')

phase_input.grid(row = 3, column = 1,pady=10)
submit_button = Button(controlPanel,text = "Generate",padx=8,pady=6,cursor='hand2', relief=FLAT,
  command=lambda: Generate()).grid(row=5,column=1)

root.mainloop()