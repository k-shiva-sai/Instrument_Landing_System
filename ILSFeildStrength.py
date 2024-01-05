from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image,ImageTk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)

class ILSFeildStrength(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.imFrame = Frame(self,height=560,width=900)
        self.labelFrame = Frame(self,height=85,width=900)
        self.controlPanel = Frame(self,bg="#3A3939",height=645,width=300)
        self.imFrame.pack(side=LEFT,fill=Y)
        self.labelFrame.place(x=0,y=590)
        #controlPanel.pack(side=RIGHT,fill=X)
        self.controlPanel.pack(side=RIGHT,fill=Y)
        self.controlPanel.pack_propagate(0)
        self.controlPanel.grid_propagate(0)
        self.controlPanel.grid_rowconfigure(0,minsize=50)
        self.electricFieldLabel = Label(self.labelFrame,text="",font=("Ubuntu",15),padx=20)
        self.electricFieldLabel.grid(row=0,column=0)
        self.twoRayImage = PhotoImage(file="assets/TwoRayModel.png")
        Label(self.imFrame, image=self.twoRayImage).grid()
        Label(self.controlPanel,text="Control Panel",fg="white",bg="#3A3939",font=("Ubuntu",18,"bold")).pack(side=TOP,fill=X)
        labelList = ["Fc (MHz)","Distance (m)","Ht (m)","Hr (m)","Hp (m)","Power i/p (w)"]
        defaultValues = [110,50000,3,3600,617,15]
        self.labelWidgets(self.controlPanel,labelList)
        var = {}
        for i in range(len(labelList)):
            var[labelList[i]] = StringVar(value=defaultValues[i])

        for i in range(len(labelList)):
            Entry(self.controlPanel,textvariable=var[labelList[i]],font=("Ubuntu",12),width=12,
        bg="#4a4848",fg="white",insertbackground="white").grid(row=i+1,column=1,padx=20,pady=6)

        submit_button = Button(self.controlPanel,text = "Generate",padx=8,pady=4,cursor='hand2', relief=FLAT,
        command=lambda: self.Generate(var)).grid(row=14,column=1)

    def Generate(self,var):
        Fc = float(var["Fc (MHz)"].get())*10**6
        D = float(var["Distance (m)"].get())/1000
        Ht = float(var["Ht (m)"].get())
        Hr = float(var["Hr (m)"].get())
        Hp = float(var["Hp (m)"].get()) #antenna base amsl
        powerInp = 20*np.log10(float(var["Power i/p (w)"].get()))
        lamda = (3*(10**8))/Fc
        Ae = 8493333            #aperture of earth
        delta = 2*Ht*(Hr - Hp - (D/4.1)**2)/(D*1000)
        X = (D/4.1)**2#(D**2)/(2*Ae)
        d = ((Hr/1000-Hp/1000-X/1000)**2 + D**2)**0.5
        C = 10*np.log10(2 - 2*np.cos(2*np.pi*delta/lamda))
        E = 76.9 + powerInp - 20*np.log10(d) + C
        print(E,C,d,X,delta)
        self.electricFieldLabel.config(text="Electric feild strength at {0:.2f} km is {1:.3f} μv/m".format(D,E))

    def labelWidgets(self,root,labelList):
        for i in range(len(labelList)):
            Label(root,text=labelList[i],bg="#3A3939",fg="white",font=("Ubuntu",15)).grid(row=i+1,padx=20,pady=6)