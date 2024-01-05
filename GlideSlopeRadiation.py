from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image,ImageTk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)

class GlideSlopeRadiation(Frame):
    antennaIsOn = [True for _ in range(20)]
    lDefaultValues = [[0.95,3.04,5.30,7.73,10.34,13.13,16.09,19.23,22.54,26.03],
    [93,100,100,93,82,66,45,29,15,11],
    [0,0,0,0,0,0,0,0,0,0]]
    rDefaultValues = [[0,0.5,1],[0,180,0]]
    rSboDefaultValues = [[0.5,1,0.5],[180,0,180]]
    leftVars = [[0 for _ in range(10)] for _ in range(3)]
    rightVars = [[0 for _ in range(3)] for _ in range(2)]
    rightSboVars = [[0 for _ in range(3)] for _ in range(2)]
    antennas = []

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.imFrame = Frame(self,height=645,width=900)
        self.controlPanel = Frame(self,bg="#3A3939",height=645,width=300)
        self.imFrame.place(x=-580,y=-685)
        self.antennaFrame = Frame(self,height=680,width=50,bg="white")
        self.antennaFrame.place(x=0,y=0)
        #controlPanel.pack(side=RIGHT,fill=X)
        self.controlPanel.pack(side=RIGHT,fill=Y)
        self.controlPanel.pack_propagate(0)
        self.controlPanel.grid_propagate(0)
        self.controlPanel.grid_rowconfigure(0,minsize=50)
        self.controlPanel.grid_columnconfigure(1, weight=1)
        self.glideImage = PhotoImage(file="assets/glidePathAntenna.png")
        Label(self.antennaFrame,image=self.glideImage).pack(side=LEFT)
        Label(self.controlPanel,text="Control Panel",fg="white",bg="#3A3939",font=("Ubuntu",18,"bold")).pack(side=TOP,fill=X)
        self.enableCsb = IntVar(value=1)
        Checkbutton(self.controlPanel, text="CSB", variable=self.enableCsb).grid(row=1,columnspan=2,pady=10)
        self.enableSbo = IntVar(value=1)
        Checkbutton(self.controlPanel, text="SBO", variable=self.enableSbo).grid(row=2,columnspan=2,pady=10)
        for i in range(2):
            for j in range(3):
                self.rightVars[i][j] = StringVar(value=self.rDefaultValues[i][j])
                self.rightSboVars[i][j] = StringVar(value=self.rSboDefaultValues[i][j])
        param_button = Button(self.controlPanel,text = "Adjust antenna \n parameters",padx=8,pady=6,cursor='hand2', relief=FLAT,
        command=self.openParametersWindow).grid(row=3,column=1,pady=10)
        submit_button = Button(self.controlPanel,text = "Generate",padx=8,pady=4,cursor='hand2', relief=FLAT,
        command=lambda: self.Generate(self.imFrame)).grid(row=4,column=1)
    
    def plotRadiation(self,imFrame,theta,Ecsb,Esbo):
        for w in imFrame.winfo_children():
            w.destroy()
        fig = plt.Figure(figsize=(20,20))
        ax=fig.add_axes([0.1,0.1,0.8,0.8],polar=True)
        ax.set_xticks(np.arange(-np.pi,np.pi,np.pi/90))
        ax.set_thetamin(90)
        ax.set_thetamax(-90)
        ax.vlines(0,0,max(max(Esbo),max(Ecsb)),colors='black', linestyles='solid')
        if self.enableCsb.get()==1:
            ax.plot(theta,Ecsb)
        if self.enableSbo.get()==1:
            ax.plot(theta,Esbo)
        canvas = FigureCanvasTkAgg(fig,imFrame)
        canvas.draw()
        wid = canvas.get_tk_widget()
        wid.place(x=0,y=0)
        toolbar = NavigationToolbar2Tk(canvas,imFrame)
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

    def Generate(self,imFrame):
        theta = np.arange(0, np.pi/4, 0.001)
        #E = 2*sin((2/2.72)*1.56*pi*sin(theta+ph)) if isOn else 2*sin(-pi/2+par*pi*sin(theta+ph)/2)
        E = None
        t = np.sin(np.deg2rad(3))
        phi = (np.pi/2)*(np.sin(theta/t))
        k = 0.117
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
        Fcsb = np.sin(phi*(np.cos(phi)-1))
        Fsbo = (0.5*np.sin(phi)-np.sin(2*phi)+0.5*np.sin(3*phi))
        # if isOn:
        #   E = sin(phi*(cos(phi)-1))
        # else:
        #   E = k*(0.5*sin(phi)-sin(2*phi)+0.5*sin(3*phi))
        Fcsb = abs(Fcsb)
        Fsbo = abs(Fsbo)
        plt.figure()
        ax1 = plt.subplot(111)
        ax1.plot(np.degrees(theta),Esu,'r')
        ax1.plot(np.degrees(theta),Esm,'g')
        ax1.plot(np.degrees(theta),Esl,'b')
        #plt.show()
        # ax2 = plt.subplot(111, projection='polar')
        # ax2.plot(theta,abs(lower),'r')
        # ax2.plot(theta,abs(middle),'g')
        # ax2.plot(theta,abs(upper),'b')
        #plt.show()
        ddm = 4*0.117*np.cos((np.pi/2)*np.sin(theta)/t)
        # plt.figure()
        # plt.plot(np.rad2deg(theta),ddm)
        # plt.grid()
        # plt.xticks(np.arange(0, 12, step=1))
        #plt.yticks(arange(-0.5, 0.5, step=0.05))
        #plt.show()

        self.plotRadiation(imFrame,theta,abs(3*Ecsb),abs(Esbo))