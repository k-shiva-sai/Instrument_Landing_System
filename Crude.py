from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image,ImageTk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)

class Crude(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.imFrame = Frame(self,height=645,width=900)
        self.controlPanel = Frame(self,bg="#3A3939",height=645,width=300)
        self.imFrame.place(x=50,y=0)
        self.localizerLabel1 = Label(self.imFrame,text="",font=("Ubuntu",15))
        self.localizerLabel2 = Label(self.imFrame,text="",font=("Ubuntu",15))
        self.glideSlopeLabel = Label(self.imFrame,text="",font=("Ubuntu",15))
        self.localizerLabel1.grid(row=0, column=0)
        self.localizerLabel2.grid(row=1, column=0)
        self.glideSlopeLabel.grid(row=2, column=0)
        self.controlPanel.pack(side=RIGHT,fill=Y)
        self.controlPanel.pack_propagate(0)
        self.controlPanel.grid_propagate(0)
        self.controlPanel.grid_rowconfigure(0,minsize=50)
        self.controlPanel.grid_columnconfigure(1, weight=1)

        self.labelList = ["Obstacle angle \n wrt Localizer", "Obstacle angle \n wrt GlideSlope","Angle wrt Runway"]
        self.defaultValues = [1,1,5]
        self.labelWidgets(self.controlPanel,self.labelList)
        self.var = {}
        for i in range(len(self.labelList)):
            self.var[i] = StringVar(value=self.defaultValues[i])

        for i in range(len(self.labelList)):
            Entry(self.controlPanel,textvariable=self.var[i],font=("Ubuntu",12),width=12,
            bg="#4a4848",fg="white",insertbackground="white").grid(row=i+1,column=1,padx=20,pady=6)
        Label(self.controlPanel,text="Control Panel",fg="white",bg="#3A3939",font=("Ubuntu",18,"bold")).pack(side=TOP,fill=X)
        submit_button = Button(self.controlPanel,text = "Generate",padx=8,pady=4,cursor='hand2', relief=FLAT,
        command=lambda: self.Generate(self.imFrame)).grid(row=5,column=1)

    def Generate(self,var):
        obsAngleLocalizer = float(self.var[0].get())
        obsAngleGLideSlope = float(self.var[1].get())
        obsAngleWrtRunway = float(self.var[2].get())
        if obsAngleWrtRunway<=10 and obsAngleLocalizer>=0.75:
            self.localizerLabel1.config(text="Obstacle will effect Lz (±10°)")
        else:
            self.localizerLabel1.config(text="Obstacle won't effect Lz (±10°)")

        if obsAngleWrtRunway<=35 and obsAngleWrtRunway>10 and obsAngleLocalizer>=1.1:
             self.localizerLabel2.config(text="Obstacle will effect Lz (± 10° to 35°)")
        else:
             self.localizerLabel2.config(text="Obstacle won't effect Lz (± 10° to 35°)")

        if obsAngleWrtRunway<=8 and obsAngleGLideSlope>=1.1:
             self.glideSlopeLabel.config(text="Obstacle will effect GS")
        else:
             self.glideSlopeLabel.config(text="Obstacle won't effect GS")   

    def labelWidgets(self,root,labelList):
        for i in range(len(labelList)):
            Label(root,text=labelList[i],bg="#3A3939",fg="white",font=("Ubuntu",12)).grid(row=i+1,padx=20,pady=6)