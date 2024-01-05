from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image,ImageTk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)

class PassiveAnalysis(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.imFrame = Frame(self,height=560,width=900)
        self.labelFrame = Frame(self,height=85,width=900)
        self.controlPanel = Frame(self,bg="#3A3939",height=645,width=300)
        self.imFrame.pack(side=LEFT,fill=Y)
        self.labelFrame.place(x=0,y=560)
        self.labelX0 = Label(self.labelFrame,text="",font=("Ubuntu",15),padx=20)
        self.labelL = Label(self.labelFrame,text="",font=("Ubuntu",15),padx=20)
        self.labelW = Label(self.labelFrame,text="",font=("Ubuntu",15),padx=20)
        self.labelX0.grid(row=0, column=0)
        self.labelL.grid(row=1, column=0)
        self.labelW.grid(row=2, column=0)
        self.controlPanel.pack(side=RIGHT,fill=Y)
        self.controlPanel.pack_propagate(0)
        self.controlPanel.grid_propagate(0)
        self.controlPanel.grid_rowconfigure(0,minsize=50)
        self.controlPanel.grid_columnconfigure(1, weight=1)
        self.passiveImage = PhotoImage(file="assets/PassiveGlideSlope.png")
        Label(self.imFrame, image=self.passiveImage).grid()
        self.labelList = ["Fc (MHz)","Distance (m)","Ht (m)","Hr (m)"]
        self.defaultValues = [330,40000,3,3000,20]
        self.labelWidgets(self.controlPanel,self.labelList)
        self.var = {}
        for i in range(len(self.labelList)):
            self.var[self.labelList[i]] = StringVar(value=self.defaultValues[i])

        for i in range(len(self.labelList)):
            Entry(self.controlPanel,textvariable=self.var[self.labelList[i]],font=("Ubuntu",12),width=12,
            bg="#4a4848",fg="white",insertbackground="white").grid(row=i+1,column=1,padx=20,pady=6)
        Label(self.controlPanel,text="Control Panel",fg="white",bg="#3A3939",font=("Ubuntu",18,"bold")).pack(side=TOP,fill=X)
        submit_button = Button(self.controlPanel,text = "Generate",padx=8,pady=4,cursor='hand2', relief=FLAT,
        command=self.Generate).grid(row=6,column=1)

    def Generate(self):
        Fc = float(self.var[self.labelList[0]].get())*10**6
        D = float(self.var[self.labelList[1]].get())/1000
        Ht = float(self.var[self.labelList[2]].get())/1000
        Hr = float(self.var[self.labelList[3]].get())/1000
        lamda = (3*(10**8))/Fc
        ang = np.arctan((Ht+Hr)/D)
        print(np.rad2deg(ang))
        Xo = D/(2 + D*ang/lamda)
        L = 2*Xo - (D/2)*((2 - 3**0.5)/(2+0.338*D*ang))
        W = (4.44/(1/D + 0.169*ang**2))**0.5
        self.labelX0.config(text="Xo: {0:.3f} m".format(Xo*1000))
        self.labelL.config(text="L: {0:.3f} m".format(L*1000))
        self.labelW.config(text="W: {0:.3f} m".format(W*1000))

    def labelWidgets(self,root,labelList):
        for i in range(len(labelList)):
            Label(root,text=labelList[i],bg="#3A3939",fg="white",font=("Ubuntu",12)).grid(row=i+1,padx=20,pady=6)