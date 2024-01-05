from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image,ImageTk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)

class SignalGeneration(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.imFrame = Frame(self,height=645,width=900)
        self.controlPanel = Frame(self,bg="#3A3939",height=645,width=300)
        self.imFrame.pack(side=LEFT,fill=Y)
        self.controlPanel.pack(side=RIGHT,fill=Y)
        #self.controlPanel.place(x=900,y=0)
        self.controlPanel.pack_propagate(0)
        self.controlPanel.grid_propagate(0)
        self.controlPanel.grid_rowconfigure(0,minsize=50)
        Label(self.controlPanel,text="Control Panel",fg="white",bg="#3A3939",font=("Ubuntu",18,"bold")).pack(side=TOP,fill=X)
        self.guidanceOrMessage = IntVar(value=1)
        Checkbutton(self.controlPanel, text="Guidance signal/Message signals", variable=self.guidanceOrMessage).grid(row=1,columnspan=2,pady=10)

        self.labelList = ["Carrier Frequency (MHz)","Message1 Frequency (Hz)","Message2 Frequency (Hz)","Amplitude of Carrier (v)","Amplitude of message1 (v)","Amplitude of message2 (v)","Modulation Index1","Modulation Index2","Time (sec)","Phase of CSB1","Phase of CSB2","Phase of SBO1","Phase of SBO2"]
        defaultValues = [0.0003,3,5,1,1,1,0.4,0.4,1,0,0,180,0]
        self.labelWidgets(self.controlPanel,self.labelList)
        var = {}
        for i in range(len(self.labelList)):
            var[self.labelList[i]] = StringVar(value=defaultValues[i])

        for i in range(len(self.labelList)):
            Entry(self.controlPanel,textvariable=var[self.labelList[i]],font=("Ubuntu",12),width=8,
        bg="#4a4848",fg="white",insertbackground="white").grid(row=i+2,column=1,padx=5,pady=6)

        submit_button = Button(self.controlPanel,text = "Generate",padx=8,pady=4,cursor='hand2', relief=FLAT,
        command=lambda: self.Generate(var)).grid(row=15,columnspan=2)
        
    def sinSignal(self,amp,freq,samples,samplingFrequency,phase):
        return amp * np.sin(phase+2*np.pi*freq*samples/samplingFrequency)

    def plot(self,samples,sps,sbo,csb):
        for w in self.imFrame.winfo_children():
            w.destroy()
        fig = plt.Figure(dpi=125)
        pltSbo = fig.add_subplot(311,title="SBO")
        pltCsb = fig.add_subplot(312,title="CSB",ylabel="Amplitude (volts)")
        pltGuide = fig.add_subplot(313,title="Guindace Signal",xlabel="Time (sec)")
        fig.tight_layout()
        pltSbo.plot(samples/sps,sbo)
        pltCsb.plot(samples/sps,csb)
        pltGuide.plot(samples/sps,sbo+csb)
        canvas = FigureCanvasTkAgg(fig,self.imFrame)
        canvas.draw()
        wid = canvas.get_tk_widget()
        wid.place(x=0,y=0)
        toolbar = NavigationToolbar2Tk(canvas,self.imFrame)
        toolbar.update()
        tool = canvas.get_tk_widget()
        tool.pack(side=BOTTOM)
    
    def plotMessage(self,samples,sps,Mc1,Ms1,Mc2,Ms2):
        for w in self.imFrame.winfo_children():
            w.destroy()
        fig = plt.Figure(dpi=125)
        pltMc1 = fig.add_subplot(221,title="Message signal1 CSB",ylabel="Amplitude (volts)")
        pltMs1 = fig.add_subplot(222,title="Message signal1 SBO")
        pltMc2 = fig.add_subplot(223,title="Message signal2 CSB",xlabel="Time (sec)")
        pltMs2 = fig.add_subplot(224,title="Message signal2 SBO")
        fig.tight_layout()
        pltMc1.plot(samples/sps,Mc1)
        pltMs1.plot(samples/sps,Ms1)
        pltMc2.plot(samples/sps,Mc2)
        pltMs2.plot(samples/sps,Ms2)
        canvas = FigureCanvasTkAgg(fig,self.imFrame)
        canvas.draw()
        wid = canvas.get_tk_widget()
        wid.place(x=0,y=0)
        toolbar = NavigationToolbar2Tk(canvas,self.imFrame)
        toolbar.update()
        tool = canvas.get_tk_widget()
        tool.pack(side=BOTTOM)

    def Generate(self,var):
        Fc = float(var[self.labelList[0]].get())*10**6
        Fm1 = float(var[self.labelList[1]].get())
        Fm2 = float(var[self.labelList[2]].get())
        Am = float(var[self.labelList[3]].get())
        Am1 = float(var[self.labelList[4]].get())
        Am2 = float(var[self.labelList[5]].get())
        m1 = float(var[self.labelList[6]].get())
        m2 = float(var[self.labelList[7]].get())
        duration = float(var[self.labelList[8]].get())
        pc1 = float(var[self.labelList[9]].get())
        pc2 = float(var[self.labelList[10]].get())
        ps1 = float(var[self.labelList[11]].get())
        ps2 = float(var[self.labelList[12]].get())

        samplingFrequency = Fc*10
        samples = np.arange(samplingFrequency*duration)
        m90c = self.sinSignal(Am1,Fm1,samples,samplingFrequency,np.radians(pc1))
        m150c = self.sinSignal(Am2,Fm2,samples,samplingFrequency,np.radians(pc2))
        m90s = self.sinSignal(Am1,Fm1,samples,samplingFrequency,np.radians(ps1))
        m150s = self.sinSignal(Am2,Fm2,samples,samplingFrequency,np.radians(ps2))
        carrier = self.sinSignal(1,Fc,samples,samplingFrequency,0)
        csb = Am*(1 + m1*m90c + m2*m150c)*carrier
        sbo = Am*(m2*m150s + m1*m90s)*carrier
        if self.guidanceOrMessage.get()==1:
            self.plot(samples,samplingFrequency,sbo,csb)
        else:
            self.plotMessage(samples,samplingFrequency,m90c,m90s,m150c,m150s)

    def labelWidgets(self,root,labelList):
        for i in range(len(labelList)):
            Label(root,text=labelList[i],bg="#3A3939",fg="white",font=("Ubuntu",13)).grid(row=i+2,padx=5,pady=6,sticky=E)