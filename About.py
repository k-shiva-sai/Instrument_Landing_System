from tkinter import *

aboutText = '''This project is carried out by Kalyan, Chethan and Shiva Sai of CBIT under the guidance of Dr. A. Supraja Reddy, 
Associate Professor, Department of ECE, CBIT and Dr. Ch. Mahesh Assistant General Manager (AGM), Communications, 
Navigation and Surveillance Systems (CNS), R&D Technical Centre, Begumpet Airport, Hyderabad
'''

class About(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.imFrame = Frame(self,height=645,width=1200)
        self.imFrame.pack(side=LEFT,fill=Y)
        textWidget = Text(self.imFrame, padx=10, height=800, width=1200)
        textWidget.pack()
        textWidget.insert(END, aboutText)
        textWidget['state'] = 'disabled'