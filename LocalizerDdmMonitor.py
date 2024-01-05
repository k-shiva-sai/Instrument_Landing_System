from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image,ImageTk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from GenericAntennaLocalizer import ScrollbarFrame

lDefaultValues = [[0.95,3.04,5.30,7.73,10.34,13.13,16.09,19.23,22.54,26.03],
[93,100,100,93,82,66,45,29,15,11],
[0,0,0,0,0,0,0,0,0,0]]
rDefaultValuesCSB = [[0.95,3.04,5.30,7.73,10.34,13.13,16.09,19.23,22.54,26.03],
[93,100,100,93,82,66,45,29,15,11],
[0,0,0,0,0,0,0,0,0,0]]
rDefaultValuesSBO = [[0.95,3.04,5.30,7.73,10.34,13.13,16.09,19.23,22.54,26.03],
[0.55,1.89,3.38,4.82,6,6.66,6.59,5.75,4.2,3.29],
[0,0,0,0,0,0,0,0,0,0]]
# rDefaultValues = [[1.90,9.54,15.82,21.8,27.8,33.8,16.09,19.23,22.54,26.03],
# [100,54.9,33.5,19,8.1,2.4,45,29,15,11],
# [0,0,0,0,0,0,0,0,0,0]]
# rDefaultValuesSBO = [[1.90,9.54,15.82,21.8,27.8,33.8,16.09,19.23,22.54,26.03],
# [7.1,5,6.72,4.88,2.61,0.9,6.59,5.75,4.2,3.29],
# [0,0,0,0,0,0,0,0,0,0]]

class LocalizerDdmMonitor(Frame):
    # antennaIsOn = [True for i in range(20)]
    # leftVars = [[0 for i in range(10)] for _ in range(3)]
    # rightVars = [[0 for i in range(10)] for _ in range(3)]
    # rSboVars = [[0 for i in range(10)] for _ in range(3)]
    # antennas = []

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.imFrame = Frame(self,height=645,width=900)
        self.controlPanel = Frame(self,bg="#3A3939",height=645,width=300)
        self.imFrame.pack(side=LEFT,fill=Y)
        #controlPanel.pack(side=RIGHT,fill=X)
        self.controlPanel.pack(side=RIGHT,fill=Y)
        self.controlPanel.pack_propagate(0)
        self.controlPanel.grid_propagate(0)
        self.controlPanel.grid_rowconfigure(0,minsize=50)
        self.controlPanel.grid_columnconfigure(1, weight=1)

        self.labelList = ["Theta range","Sector width","Required DDM","Current DDM","DDM at 0°","AF CSB","AF SBO","Req AF SBO","Antenna Pairs(n)"]
        defaultValues = [10,2,0.155,None,None,None,None,None,10]
        self.leftVars, self.lSboVars, self.rightVars, self.rSboVars = [],[],[],[]
        self.leftButtons = []
        self.rightButtons = []
        self.labelWidgets(self.controlPanel,self.labelList)
        self.var = {}
        for i in range(len(self.labelList)):
            self.var[self.labelList[i]] = StringVar(value=defaultValues[i])

        for i in range(len(self.labelList)):
            state = DISABLED if i > 2 and i < 8 else None
            Entry(self.controlPanel,textvariable=self.var[self.labelList[i]],font=("Ubuntu",11),width=20, state = state,
            bg="#4a4848",fg="white",insertbackground="white").grid(row=i+1,column=1,padx=20,pady=6)

        Label(self.controlPanel,text="Control Panel",fg="white",bg="#3A3939",font=("Ubuntu",18,"bold")).pack(side=TOP,fill=X)
        # antennaOnImage = PhotoImage(file="assets/antenna_on.png")
        # antennaOffImage = PhotoImage(file="assets/antenna_off.png")
        # for i in range(3):
        #     for j in range(10):
        #         self.leftVars[i][j] = StringVar(value=self.lDefaultValues[i][j])
        #         self.rightVars[i][j] = StringVar(value=self.rDefaultValues[i][j])
        #         self.rSboVars[i][j] = StringVar(value=self.rDefaultValuesSBO[i][j])
        # for i in range(len(self.antennaIsOn)):
        #     img = antennaOnImage if self.antennaIsOn[i]  else antennaOffImage
        #     self.antennas.append(Button(self.antennaFrame,image=img,bd=0,command=lambda c = i: self.antennaCommand(c,antennaOffImage,antennaOnImage)))
        #     self.antennas[i].pack(side=TOP)
        param_button = Button(self.controlPanel,text = "Adjust antenna \n parameters",padx=8,pady=6,cursor='hand2', relief=FLAT,
        command=self.openParametersWindow).grid(row=10,columnspan=2,pady=10)
        submit_button = Button(self.controlPanel,text = "Generate",padx=8,pady=4,cursor='hand2', relief=FLAT,
        command=lambda: self.Generate(self.imFrame)).grid(row=11,columnspan=2)
    
    def plotDdmMonitoring(self,imFrame,theta,Ecsb,Esbo,Ddm):
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
    
    def openParametersWindow(self):
        newWindow = Toplevel(bg="#3A3939")
        newWindow.title("Localizer antenna parameters")
        # newWindow.geometry("600x300")
        # newWindow.grid_rowconfigure(10,minsize=50)
        sbf = ScrollbarFrame(newWindow,270,400)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        sbf.grid(row=0, column=0, sticky='nsew')

        antennaCount = int(self.var[self.labelList[8]].get())
        if antennaCount <= 10:
            self.leftVars = [[StringVar(value=rDefaultValuesCSB[i][j]) for j in range(antennaCount)] for i in range(3)]
            self.lSboVars = [[StringVar(value=rDefaultValuesSBO[i][j]) for j in range(antennaCount)] for i in range(3)]
            self.rightVars = [[StringVar(value=rDefaultValuesCSB[i][j]) for j in range(antennaCount)] for i in range(3)]
            self.rSboVars = [[StringVar(value=rDefaultValuesSBO[i][j]) for j in range(antennaCount)] for i in range(3)]
        else:
            self.leftVars = [[StringVar(value=0) for _ in range(antennaCount)] for _ in range(3)]
            self.lSboVars = [[StringVar(value=0) for _ in range(antennaCount)] for _ in range(3)]
            self.rightVars = [[StringVar(value=0) for _ in range(antennaCount)] for _ in range(3)]
            self.rSboVars = [[StringVar(value=0) for _ in range(antennaCount)] for _ in range(3)]
        frame = sbf.scrolled_frame
        Label(frame,text="Left",bg="#3A3939",fg="white",font=("Ubuntu",10)).grid(row=1,column=0)
        Label(frame,text="Right",bg="#3A3939",fg="white",font=("Ubuntu",10)).grid(row=2,column=0)
        Label(frame,text="CSB",bg="#3A3939",fg="white",font=("Ubuntu",10)).grid(row=3,column=0)

        Label(frame,text="Distance",bg="#3A3939",fg="white",font=("Ubuntu",10)).grid(row=4,column=0)
        Label(frame,text="Amplitude",bg="#3A3939",fg="white",font=("Ubuntu",10)).grid(row=5,column=0)
        Label(frame,text="Phase",bg="#3A3939",fg="white",font=("Ubuntu",10)).grid(row=6,column=0)
        for i in range(3):
            for j in  range(len(self.rightVars[0])):
                Entry(frame,textvariable=self.rightVars[i][j],width=8,bg="#4a4848",fg="white",insertbackground="white").grid(row=i+4,column=j+1)
                Entry(frame,textvariable=self.rSboVars[i][j],width=8,bg="#4a4848",fg="white",insertbackground="white").grid(row=i+8,column=j+1)
        
        Label(frame,text="SBO",bg="#3A3939",fg="white",font=("Ubuntu",10)).grid(row=7,column=0)
        self.leftButtons = []
        self.rightButtons = []
        for i in range(len(self.rightVars[0])):
            self.leftButtons.append(Button(frame,text="ON", width=10,bg='light green', command=lambda c = i: self.Toggle(c,True)))
            self.leftButtons[i].grid(row=1,column=i+1)
            self.rightButtons.append(Button(frame,text="ON", width=10,bg='light green', command=lambda c = i: self.Toggle(c,False)))
            self.rightButtons[i].grid(row=2,column=i+1)
            Label(frame,text="A"+str(i+1),bg="#3A3939",fg="white").grid(row=0,column=i+1)
            Label(frame,text="A"+str(i+1),bg="#3A3939",fg="white").grid(row=3,column=i+1)
            Label(frame,text="A"+str(i+1),bg="#3A3939",fg="white").grid(row=7,column=i+1)
        Label(frame,text="Distance",bg="#3A3939",fg="white",font=("Ubuntu",10)).grid(row=8,column=0)
        Label(frame,text="Amplitude",bg="#3A3939",fg="white",font=("Ubuntu",10)).grid(row=9,column=0)
        Label(frame,text="Phase",bg="#3A3939",fg="white",font=("Ubuntu",10)).grid(row=10,column=0)            


    def fTheta(self,t):
        return pow(10,-(0.0000442*pow(abs(t),3)+0.0023678*pow(abs(t),2)+0.016252*abs(t))/20)

    def call_Ddm(self,th):
        Ec,Es = 0,0
        for i in range(len(self.rightVars[0])):
            isLeftOn, isRightOn = self.leftButtons[i]['text']=='ON', self.rightButtons[i]['text']=='ON'
            var = int(isLeftOn) + int(isRightOn)
            dist,amp,phase = float(self.rightVars[0][i].get()),float(self.rightVars[1][i].get()),np.radians(float(self.rightVars[2][i].get()))
            sboDist,sboAmp,sboPhase = float(self.rSboVars[0][i].get()),float(self.rSboVars[1][i].get()),np.radians(float(self.rSboVars[2][i].get()))
            Ec += var*amp*(np.cos((1/2.72)*dist*np.pi*np.sin(th+phase)))
            Es += var*sboAmp*((np.sin((1/2.72)*sboDist*np.pi*np.sin(th+sboPhase))))
        return [2*Es/Ec,abs(Ec),abs(Es)]

    def Generate(self,imFrame):
        limit = float(self.var[self.labelList[0]].get())
        sectorWidth = float(self.var[self.labelList[1]].get())
        reqDdm = float(self.var[self.labelList[2]].get())
        # curDdm = float(self.var[self.labelList[3]].get())
        # afCsb = float(self.var[self.labelList[4]].get())
        # afSbo = float(self.var[self.labelList[5]].get())
        # reqAfSbo = float(self.var[self.labelList[6]].get())
        theta = np.arange(0, np.deg2rad(limit)+0.0001, 0.005)

        Ecsb=0*theta
        Esbo=0*theta
        ang = np.radians(sectorWidth/2)
        for i in range(len(self.rightVars[0])):
            isLeftOn, isRightOn = self.leftButtons[i]['text']=='ON', self.rightButtons[i]['text']=='ON'
            var = int(isLeftOn) + int(isRightOn)
            dist,amp,phase = float(self.rightVars[0][i].get()),float(self.rightVars[1][i].get()),np.radians(float(self.rightVars[2][i].get()))
            sboDist,sboAmp,sboPhase = float(self.rSboVars[0][i].get()),float(self.rSboVars[1][i].get()),np.radians(float(self.rSboVars[2][i].get()))
            
            Ecsb += var*amp*(np.cos((1/2.72)*dist*np.pi*np.sin(theta+phase)))*self.fTheta(theta)
            Esbo += var*sboAmp*self.fTheta(theta)*((np.sin((1/2.72)*sboDist*np.pi*np.sin(theta+sboPhase))))
        
        ddmRes = self.call_Ddm(ang)
        self.var[self.labelList[3]].set(round(ddmRes[0],3))
        self.var[self.labelList[4]].set(round(self.call_Ddm(0)[0],3))
        self.var[self.labelList[5]].set(round(ddmRes[1],3))
        self.var[self.labelList[6]].set(round(ddmRes[2],3))
        self.var[self.labelList[7]].set(round(reqDdm*ddmRes[1]/2,3))
        print(ddmRes[1]*self.fTheta(ang))
        # for i in np.arange(0,20,0.01):
        #   d = cal_Ddm(np.deg2rad(i))
        #   if d<0.1559 and d>0.15499:
        #     print(i,d)
        #     break

        ddm = 2*Esbo/Ecsb

        Ecsb = abs(Ecsb)
        Esbo = abs(Esbo)
        #f(o) phi amp
        self.plotDdmMonitoring(imFrame,theta,Ecsb,Esbo,ddm)

    def Toggle(self,i,isLeft):
        print(i,len(self.leftButtons),isLeft)
        button = self.leftButtons[i] if isLeft else self.rightButtons[i]
        if button.config('text')[-1] == 'ON':
            button.config(text='OFF', bg='orange red')
        else:
            button.config(text='ON',bg='light green')
        print(button['text'])
    def antennaCommand(self,i,antennaOffImage,antennaOnImage):
        j = len(self.antennaIsOn)-i-1
        if self.antennaIsOn[i]:
            self.antennas[i].config(image=antennaOffImage)
            self.antennas[j].config(image=antennaOffImage)
        else:
            self.antennas[i].config(image=antennaOnImage)
            self.antennas[j].config(image=antennaOnImage)
        self.antennaIsOn[i] = not self.antennaIsOn[i]
        self.antennaIsOn[j] = not self.antennaIsOn[j]

    def labelWidgets(self,root,labelList):
        for i in range(len(labelList)):
            Label(root,text=labelList[i],bg="#3A3939",fg="white",font=("Ubuntu",15)).grid(row=i+1,padx=20,pady=6)

    def enableOutputWidgets(self):
        for i in self.outputTextWidgetsIdxs:
            self.var[self.labelList[i]].configure(state='disabled')

    def disableOutputWidgets(self):
        for i in self.outputTextWidgetsIdxs:
            self.var[self.labelList[i]].configure(state='enabled')