from struct import pack
from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image,ImageTk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)

class GlideSlopeDdmMonitor(Frame):
    antennaIsOn = [True for _ in range(20)]
    lDefaultValues = [[0.95,3.04,5.30,7.73,10.34,13.13,16.09,19.23,22.54,26.03],
    [93,100,100,93,82,66,45,29,15,11],
    [0,0,0,0,0,0,0,0,0,0]]
    rDefaultValues = [[1,0,0],[0,180,0]]
    rSboDefaultValues = [[0,0.117,0],[180,180,180]]
    leftVars = [[0 for _ in range(10)] for _ in range(3)]
    rightVars = [[0 for _ in range(3)] for _ in range(2)]
    rightSboVars = [[0 for _ in range(3)] for _ in range(2)]
    antennas = []

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.imFrame = Frame(self,height=645,width=900)
        self.controlPanel = Frame(self,bg="#3A3939",height=645,width=300)
        self.imFrame.pack(side=LEFT,fill=Y)
        #self.imFrame.pack(side=LEFT,fill=Y)
        #controlPanel.pack(side=RIGHT,fill=X)
        self.controlPanel.pack(side=RIGHT,fill=Y)
        self.controlPanel.pack_propagate(0)
        self.controlPanel.grid_propagate(0)
        self.controlPanel.grid_rowconfigure(0,minsize=50)
        self.controlPanel.grid_columnconfigure(1, weight=1)
        self.labelList = ["Theta range","Sector width","Elevation Angle°","Req DDM","Cur DDM","AF CSB","AF SBO","Req AF SBO"]
        defaultValues = [10,0.72,3,0.087,0,0,0,0]
        self.labelWidgets(self.controlPanel,self.labelList)
        self.var = {}
        for i in range(len(self.labelList)):
            self.var[self.labelList[i]] = StringVar(value=defaultValues[i])

        for i in range(len(self.labelList)):
            Entry(self.controlPanel,textvariable=self.var[self.labelList[i]],font=("Ubuntu",12),width=12,
            bg="#4a4848",fg="white",insertbackground="white").grid(row=i+1,column=1,padx=20,pady=6)
        Label(self.controlPanel,text="Control Panel",fg="white",bg="#3A3939",font=("Ubuntu",18,"bold")).pack(side=TOP,fill=X)
        for i in range(2):
            for j in range(3):
                self.rightVars[i][j] = StringVar(value=self.rDefaultValues[i][j])
                self.rightSboVars[i][j] = StringVar(value=self.rSboDefaultValues[i][j])
        param_button = Button(self.controlPanel,text = "Adjust antenna \n parameters",padx=8,pady=6,cursor='hand2', relief=FLAT,
        command=self.openParametersWindow).grid(row=9,column=1,pady=10)
        submit_button = Button(self.controlPanel,text = "Generate",padx=8,pady=4,cursor='hand2', relief=FLAT,
        command= self.Generate).grid(row=10,column=1)
    
    def plotRadiation(self,theta,Ecsb,Esbo):
        for w in self.imFrame.winfo_children():
            w.destroy()
        fig = plt.Figure(dpi=125)
        pltSignal = fig.add_subplot(211)
        pltGuide = fig.add_subplot(212,xlabel="Theta",ylabel="DDM")
        fig.tight_layout()
        pltSignal.plot(theta,Ecsb,'r',label='CSB')
        pltSignal.plot(theta,Esbo,'g',label='SBO')
        pltSignal.legend()
        pltGuide.plot(theta,2*Esbo/Ecsb)
        canvas = FigureCanvasTkAgg(fig,self.imFrame)
        canvas.draw()
        wid = canvas.get_tk_widget()
        wid.place(x=0,y=0)
        toolbar = NavigationToolbar2Tk(canvas,self.imFrame)
        toolbar.update()
        tool = canvas.get_tk_widget()
        tool.pack(side=RIGHT)
    
    def openParametersWindow(self):
        newWindow = Toplevel(bg="#3A3939")
        newWindow.title("GlideSlope antenna parameters")
        newWindow.geometry("300x200")
        Label(newWindow,text="CSB",bg="#3A3939",fg="white").grid(row=0,column=0)
        Label(newWindow,text="Amplitude",bg="#3A3939",fg="white").grid(row=1,column=0)
        Label(newWindow,text="Phase",bg="#3A3939",fg="white").grid(row=2,column=0)
        Label(newWindow,text="Lower",bg="#3A3939",fg="white").grid(row=0,column=1)
        Label(newWindow,text="Middle",bg="#3A3939",fg="white").grid(row=0,column=2)
        Label(newWindow,text="Upper",bg="#3A3939",fg="white").grid(row=0,column=3)
        for i in range(2):
            for j in  range(3):
                Entry(newWindow,textvariable=self.rightVars[i][j],width=8,bg="#4a4848",fg="white",insertbackground="white").grid(row=i+1,column=j+1)

        Label(newWindow,text="SBO",bg="#3A3939",fg="white").grid(row=5,column=0)
        Label(newWindow,text="Amplitude",bg="#3A3939",fg="white").grid(row=6,column=0)
        Label(newWindow,text="Phase",bg="#3A3939",fg="white").grid(row=7,column=0)
        Label(newWindow,text="Lower",bg="#3A3939",fg="white").grid(row=5,column=1)
        Label(newWindow,text="Middle",bg="#3A3939",fg="white").grid(row=5,column=2)
        Label(newWindow,text="Upper",bg="#3A3939",fg="white").grid(row=5,column=3)
        for i in range(2):
            for j in  range(3):
                Entry(newWindow,textvariable=self.rightSboVars[i][j],width=8,bg="#4a4848",fg="white",insertbackground="white").grid(row=i+6,column=j+1)

    def fTheta(self,t):
        return pow(10,-(0.0000442*pow(abs(t),3)+0.0023678*pow(abs(t),2)+0.016252*abs(t))/20)

    def generateDdm(self,theta):
        t = np.sin(np.deg2rad(float(self.var[self.labelList[2]].get())))
        Ecl = float(self.rightVars[0][0].get())*np.sin(0.5*np.pi*np.sin(theta + np.radians(float(self.rightVars[1][0].get())))/t)*2
        Ecm = float(self.rightVars[0][1].get())*np.sin(np.pi*np.sin(theta + np.radians(float(self.rightVars[1][1].get())))/t)*2
        Ecu = float(self.rightVars[0][2].get())*np.sin(1.5*np.pi*np.sin(theta + np.radians(float(self.rightVars[1][2].get())))/t)*2
        Esl = float(self.rightSboVars[0][0].get())*np.sin(0.5*np.pi*np.sin(theta + np.radians(float(self.rightSboVars[1][0].get())))/t)*2
        Esm = float(self.rightSboVars[0][1].get())*np.sin(np.pi*np.sin(theta + np.radians(float(self.rightSboVars[1][1].get())))/t)*2
        Esu = float(self.rightSboVars[0][2].get())*np.sin(1.5*np.pi*np.sin(theta + np.radians(float(self.rightSboVars[1][2].get())))/t)*2
        lower = Ecl + Esl
        middle = Ecm + Esm
        upper = Ecu + Esu
        Ecsb = Ecl + Ecm + Ecu
        Esbo = Esl + Esm + Esu
        return (2*Esbo/Ecsb,Ecsb,Esbo)

    def Generate(self):
        reqDdm = float(self.var[self.labelList[3]].get())
        t = np.sin(np.deg2rad(float(self.var[self.labelList[2]].get())))
        theta = np.arange(0, np.deg2rad(float(self.var[self.labelList[0]].get())), 0.001)
        ddmRes = self.generateDdm(t+np.deg2rad(float(self.var[self.labelList[1]].get()))/2)
        signalRes = self.generateDdm(theta)
        self.var[self.labelList[4]].set(round(ddmRes[0],3))
        self.var[self.labelList[5]].set(round(ddmRes[1],3))
        self.var[self.labelList[6]].set(round(ddmRes[2],3))
        self.var[self.labelList[7]].set(round(reqDdm*ddmRes[1]/2,3))
        self.plotRadiation(np.degrees(theta),signalRes[1],signalRes[2])

    def labelWidgets(self,root,labelList):
        for i in range(len(labelList)):
            Label(root,text=labelList[i],bg="#3A3939",fg="white",font=("Ubuntu",15)).grid(row=i+1,padx=20,pady=6)