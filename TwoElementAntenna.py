from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image,ImageTk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)

class TwoElementAtenna(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.imFrame = Frame(self,height=645,width=900)
        self.controlPanel = Frame(self,bg="#3A3939",height=645,width=300)
        self.imFrame.place(x=0,y=0)
        self.antennaFrame = Frame(self,height=680,width=50)
        self.antennaFrame.place(x=0,y=0)
        #controlPanel.pack(side=RIGHT,fill=X)
        self.controlPanel.pack(side=RIGHT,fill=Y)
        self.controlPanel.pack_propagate(0)
        self.controlPanel.grid_propagate(0)
        self.controlPanel.grid_rowconfigure(0,minsize=50)
        self.controlPanel.grid_columnconfigure(1, weight=1)

        self.leftSwitch = PhotoImage(file='assets/offState.png')
        self.rightSwitch = PhotoImage(file='assets/onState.png')
        self.isOn = True
        Label(self.controlPanel,text="Control Panel",fg="white",bg="#3A3939",font=("Ubuntu",18,"bold")).pack(side=TOP,fill=X)
        self.switch = Button(self.controlPanel,image=self.rightSwitch,bd=0,highlightthickness=0,relief=SUNKEN,padx=0,pady=0,bg="#3A3939",command=self.buttonPressed)
        self.switch.grid(row=1,column=1)
        Label(self.controlPanel, text="Out Phase",bg="#3A3939",fg="white").grid(row=1,column=0,sticky='e')
        Label(self.controlPanel, text="In Phase",bg="#3A3939",fg="white").grid(row=1,column=2)
        
        Label(self.controlPanel, text="Distance (m)",font=("Ubuntu",15),width=12,bg="#3A3939",fg="white").grid(row=2, column=0)
        self.length_input = StringVar(value=0)
        Entry(self.controlPanel,textvariable=self.length_input,font=("Ubuntu",12),width=8,bg="#4a4848",fg="white",insertbackground="white").grid(row = 2, column = 1,pady=10)

        Label(self.controlPanel, text="Phase",font=("Ubuntu",15),width=12,bg="#3A3939",fg="white").grid(row=3, column=0)
        self.phase_input = StringVar(value=0)
        Entry(self.controlPanel,textvariable=self.phase_input,font=("Ubuntu",12),width=8,bg="#4a4848",fg="white",insertbackground="white").grid(row = 3, column = 1,pady=10)
        submit_button = Button(self.controlPanel,text = "Generate",padx=8,pady=6,cursor='hand2', relief=FLAT,
        command=self.Generate).grid(row=5,column=1)
    
    def plotRadiation(self,theta,E):
        for w in self.imFrame.winfo_children():
            w.destroy()
        fig = plt.Figure(dpi=125)
        ax=fig.add_axes([0.1,0.1,0.8,0.8],polar=True)
        #   ax.set_thetamin(90)
        #   ax.set_thetamax(-90)
        ax.set_yticks([0,0.2,0.4,0.6,0.8,1])
        print(len(E))
        ax.plot(theta,E)
        canvas = FigureCanvasTkAgg(fig,self.imFrame)
        canvas.draw()
        wid = canvas.get_tk_widget()
        wid.place(x=0,y=0)
        toolbar = NavigationToolbar2Tk(canvas,self.imFrame)
        toolbar.update()
        tool = canvas.get_tk_widget()
        tool.pack(side=RIGHT)

    def fTheta(self,t):
        return pow(10,-(0.0000442*pow(abs(t),3)+0.0023678*pow(abs(t),2)+0.016252*abs(t))/20)

    def Generate(self):
        par = float(self.length_input.get())
        ph = float(self.phase_input.get())
        ph = np.radians(ph)
        theta = np.arange(-np.pi, np.pi, 0.01)
        E = None
        if self.isOn:
            E = np.cos(np.pi*par*np.sin(theta-ph))
        else:
            E = np.sin(np.pi*par*np.sin(theta-ph))
            E = abs(E)
        self.plotRadiation(theta,E)


    def buttonPressed(self):
        if self.isOn:
            self.switch.config(image=self.leftSwitch)
        else:
            self.switch.config(image=self.rightSwitch)
        self.isOn = not self.isOn