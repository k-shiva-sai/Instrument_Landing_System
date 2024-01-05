from tkinter import *
from tkinter.font import Font
from SignalGeneration import SignalGeneration
from LocalizerRadiation import LocalizerRadiation
from GlideSlopeRadiation import GlideSlopeRadiation
from LocalizerDdmMonitor import LocalizerDdmMonitor
from ObsAnalysisLZ import ObsAnalysisLZ
from ILSFeildStrength import ILSFeildStrength
from GenericAntennaLocalizer import GenericAntennaLocalizer
from Crude import Crude
from GlideSlopeDdmMonitor import GlideSlopeDdmMonitor
from PassiveAnalysis import PassiveAnalysis
from TwoElementAntenna import TwoElementAtenna
from About import About


class InstrumentLandingSystem(Tk):

  def __init__(self, *args, **kwargs):
    Tk.__init__(self, *args, **kwargs)
    self.geometry("1200x680")
    self.title("Instrument Landing System")
    self.title_font = Font(family='Helvetica',
                           size=18,
                           weight="bold",
                           slant="italic")
    top = Frame(self, bg="#9C4242", height=35, width=1200)
    top.pack(side=TOP, fill=X)

    generic = ["SignalGeneration", "TwoElementAtenna", "ILSFeildStrength"]
    localizer = [
      "LocalizerRadiation", "LocalizerDdmMonitor", "GenericAntennaLocalizer",
      "ObsAnalysisLZ", "Crude"
    ]
    glideSlope = [
      "GlideSlopeRadiation", "GlideSlopeDdmMonitor", "PassiveAnalysis"
    ]
    clicked1 = StringVar()
    clicked1.set("SignalGeneration")
    drop1 = OptionMenu(top, clicked1, *generic)
    drop1.pack(side=LEFT)
    Button(top, text="Open",
           command=lambda: self.show_frame(clicked1.get())).pack(side=LEFT)

    clicked2 = StringVar()
    clicked2.set("LocalizerRadiation")
    drop2 = OptionMenu(top, clicked2, *localizer)
    drop2.pack(side=LEFT)
    Button(top, text="Open",
           command=lambda: self.show_frame(clicked2.get())).pack(side=LEFT)

    clicked3 = StringVar()
    clicked3.set("GlideSlopeRadiation")
    drop3 = OptionMenu(top, clicked3, *glideSlope)
    drop3.pack(side=LEFT)
    Button(top, text="Open",
           command=lambda: self.show_frame(clicked3.get())).pack(side=LEFT)

    Button(top, text="About",
           command=lambda: self.show_frame("About")).pack(side=LEFT)
    container = Frame(self, bg='white')
    container.pack(side=TOP, fill="both", expand=True)
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    self.frames = {}
    for F in (LocalizerRadiation, SignalGeneration, GlideSlopeRadiation,
              LocalizerDdmMonitor, ObsAnalysisLZ, ILSFeildStrength,
              GenericAntennaLocalizer, Crude, GlideSlopeDdmMonitor,
              PassiveAnalysis, TwoElementAtenna, About):
      page_name = F.__name__
      frame = F(parent=container, controller=self)
      self.frames[page_name] = frame
      frame.grid(row=0, column=0, sticky="nsew")

    self.show_frame("SignalGeneration")

  def show_frame(self, page_name):
    '''Show a frame for the given page name'''
    frame = self.frames[page_name]
    frame.tkraise()


class PageTwo(Frame):

  def __init__(self, parent, controller):
    Frame.__init__(self, parent)
    self.controller = controller
    label = Label(self, text="This is page 2", font=controller.title_font)
    label.pack(side="top", fill="x", pady=10)
    button = Button(self,
                    text="Go to the start page",
                    command=lambda: controller.show_frame("SignalGeneration"))
    button.pack()


if __name__ == "__main__":
  app = InstrumentLandingSystem()
  app.mainloop()
