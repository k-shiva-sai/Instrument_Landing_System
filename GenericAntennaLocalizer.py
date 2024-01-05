from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image,ImageTk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)

class GenericAntennaLocalizer(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.imFrame = Frame(self,height=645,width=900)
        self.controlPanel = Frame(self,bg="#3A3939",height=645,width=300)
        self.imFrame.place(x=-580,y=-685)
        self.antennaFrame = Frame(self,height=680,width=50)
        self.antennaFrame.place(x=0,y=0)
        #controlPanel.pack(side=RIGHT,fill=X)
        self.controlPanel.pack(side=RIGHT,fill=Y)
        self.controlPanel.pack_propagate(0)
        self.controlPanel.grid_propagate(0)
        self.controlPanel.grid_rowconfigure(0,minsize=50)
        self.controlPanel.grid_columnconfigure(1, weight=1)

        self.rightVars = []
        self.rSboVars = []
        Label(self.controlPanel,text="Control Panel",fg="white",bg="#3A3939",font=("Ubuntu",18,"bold")).pack(side=TOP,fill=X)
        self.antennaCountVar = StringVar(value=0)
        Label(self.controlPanel,text="Antenna Pairs(n)",bg="#3A3939",fg="white",font=("Ubuntu",12)).grid(row=1,column=1)
        Entry(self.controlPanel,textvariable=self.antennaCountVar,width=8,bg="#4a4848",fg="white",insertbackground="white").grid(row=1,column=2)
        param_button = Button(self.controlPanel,text = "Adjust antenna \n parameters",padx=8,pady=6,cursor='hand2', relief=FLAT,
        command=self.openParametersWindow).grid(row=2,column=1,pady=10)
        submit_button = Button(self.controlPanel,text = "Generate",padx=8,pady=4,cursor='hand2', relief=FLAT,
        command=self.Generate).grid(row=3,column=1)
    
    def plotRadiation(self,theta,Ecsb,Esbo):
        for w in self.imFrame.winfo_children():
            w.destroy()
        fig = plt.Figure(figsize=(20,20))
        ax=fig.add_axes([0.1,0.1,0.8,0.8],polar=True)
        ax.set_xticks(np.arange(-np.pi,np.pi,np.pi/90))
        ax.set_thetamin(90)
        ax.set_thetamax(-90)
        ax.plot(theta,Ecsb)
        ax.plot(theta,Esbo)
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
        newWindow.title("Localizer antenna parameters")
        #newWindow.geometry("200x400")
        sbf = ScrollbarFrame(newWindow,200,400)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        sbf.grid(row=0, column=0, sticky='nsew')
        # sbf.pack(side="top", fill="both", expand=True)
        
        self.rightVars = [[StringVar() for _ in range(int(self.antennaCountVar.get()))] for _ in range(3)]
        self.rSboVars = [[StringVar() for _ in range(int(self.antennaCountVar.get()))] for _ in range(3)]
        # Some data, layout into the sbf.scrolled_frame
        frame = sbf.scrolled_frame
        Label(frame,text="CSB",bg="#3A3939",fg="white",font=("Ubuntu",10)).grid(row=0,column=0)
        Label(frame,text="Distance",bg="#3A3939",fg="white",font=("Ubuntu",10)).grid(row=1,column=0)
        Label(frame,text="Amplitude",bg="#3A3939",fg="white",font=("Ubuntu",10)).grid(row=2,column=0)
        Label(frame,text="Phase",bg="#3A3939",fg="white",font=("Ubuntu",10)).grid(row=3,column=0)
        for i in range(len(self.rightVars[0])):
            Label(frame,text="A"+str(i+1),bg="#3A3939",fg="white").grid(row=0,column=i+1)
        for i in range(3):
            for j in  range(len(self.rightVars[0])):
                Entry(frame,textvariable=self.rightVars[i][j],width=8,bg="#4a4848",fg="white",insertbackground="white").grid(row=i+1,column=j+1)
        
        Label(frame,text="SBO",bg="#3A3939",fg="white",font=("Ubuntu",10)).grid(row=4,column=0)
        Label(frame,text="Distance",bg="#3A3939",fg="white",font=("Ubuntu",10)).grid(row=5,column=0)
        Label(frame,text="Amplitude",bg="#3A3939",fg="white",font=("Ubuntu",10)).grid(row=6,column=0)
        Label(frame,text="Phase",bg="#3A3939",fg="white",font=("Ubuntu",10)).grid(row=7,column=0)
        for i in range(len(self.rightVars[0])):
            Label(frame,text="A"+str(i+1),bg="#3A3939",fg="white").grid(row=4,column=i+1)
        for i in range(3):
            for j in  range(len(self.rightVars[0])):
                Entry(frame,textvariable=self.rSboVars[i][j],width=8,bg="#4a4848",fg="white",insertbackground="white").grid(row=i+5,column=j+1)

    def fTheta(self,t):
        return pow(10,-(0.0000442*pow(abs(t),3)+0.0023678*pow(abs(t),2)+0.016252*abs(t))/20)

    def Generate(self):
        theta = np.arange(-np.pi/4, np.pi/4, 0.005)
        Ecsb = 0*theta
        Esbo=0*theta
        # Frp = 0*theta
        # Rp,Th,Phi = 4260,2,0
        print()
        for i in range(len(self.rightVars[0])):
            dist,amp,phase = float(self.rightVars[0][i].get()),float(self.rightVars[1][i].get()),np.radians(float(self.rightVars[2][i].get()))
            sboDist,sboAmp,sboPhase = float(self.rSboVars[0][i].get()),float(self.rSboVars[1][i].get()),np.radians(float(self.rSboVars[2][i].get()))
            Ecsb += 2*amp*(np.cos((2/2.72)*dist*np.pi*np.sin(theta)))*self.fTheta(theta+phase)
            Esbo += 2*sboAmp*(np.sin((2/2.72)*sboDist*np.pi*np.sin(theta+sboPhase)))*self.fTheta(theta)
        Esbo = abs(Esbo)
        Ecsb = abs(Ecsb)
        self.plotRadiation(theta,Ecsb,Esbo)

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

class ScrollbarFrame(Frame):
    def __init__(self, parent, height, width, **kwargs):
        Frame.__init__(self, parent, **kwargs)

        # The Scrollbar, layout to the right
        hsb = Scrollbar(self, orient="horizontal")
        hsb.pack(side="bottom", fill="x")

        # The Canvas which supports the Scrollbar Interface, layout to the left
        self.canvas = Canvas(self, borderwidth=0, background="#3A3939",height=height,width=width)
        self.canvas.pack(side="top", fill="both", expand=True)

        # Bind the Scrollbar to the self.canvas Scrollbar Interface
        self.canvas.configure(xscrollcommand=hsb.set)
        hsb.configure(command=self.canvas.xview)

        # The Frame to be scrolled, layout into the canvas
        # All widgets to be scrolled have to use this Frame as parent
        self.scrolled_frame = Frame(self.canvas, background=self.canvas.cget('bg'),height=height,width=width)
        self.canvas.create_window((4, 4), window=self.scrolled_frame, anchor="nw")

        # Configures the scrollregion of the Canvas dynamically
        self.scrolled_frame.bind("<Configure>", self.on_configure)

    def on_configure(self, event):
        """Set the scroll region to encompass the scrolled frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))