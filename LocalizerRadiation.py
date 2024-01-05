from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)

lDefaultValuesSelex = [[
  0.818, 2.862, 4.906, 6.950, 8.994, 11.038, 13.082, 0, 0, 0
], [0.9432, 1, 0.6746, 0.4270, 0.1616, 0.0460, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

lDefaultValuesSBOSelex = [[
  0.818, 2.862, 4.906, 6.950, 8.994, 11.038, 13.082, 0, 0, 0
], [0.2329, 0.6147, 0.9400, 1, 0.9213, 0.6463, 0.4122, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

rDefaultValuesSelex = [[
  0.818, 2.862, 4.906, 6.950, 8.994, 11.038, 13.082, 0, 0, 0
], [0.9432, 1, 0.6746, 0.4270, 0.1616, 0.0460, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

rDefaultValuesSBOSelex = [[
  0.818, 2.862, 4.906, 6.950, 8.994, 11.038, 13.082, 0, 0, 0
], [0.2329, 0.6147, 0.9400, 1, 0.9213, 0.6463, 0.4122, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

lDefaultValuesSelexClearance = [[
  0.818, 2.862, 4.906, 6.950, 8.994, 11.038, 13.082, 0, 0, 0
], [1, 0.0941, 0, 0.2072, 0.0787, 0, 0, 0, 0, 0],
                                [0, 180, 0, 180, 180, 0, 0, 0, 0, 0]]

lDefaultValuesSBOSelexClearance = [[
  0.818, 2.862, 4.906, 6.950, 8.994, 11.038, 13.082, 0, 0, 0
], [1, 0.5678, 0.289, 0.1626, 0.0699, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 180, 0, 0, 0, 0]]

rDefaultValuesSelexClearance = [[
  0.818, 2.862, 4.906, 6.950, 8.994, 11.038, 13.082, 0, 0, 0
], [1, 0.0941, 0, 0.2072, 0.0787, 0, 0, 0, 0, 0],
                                [0, 180, 0, 180, 180, 0, 0, 0, 0, 0]]

rDefaultValuesSBOSelexClearance = [[
  0.818, 2.862, 4.906, 6.950, 8.994, 11.038, 13.082, 0, 0, 0
], [1, 0.5678, 0.289, 0.1626, 0.0699, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 180, 0, 0, 0, 0]]


class LocalizerRadiation(Frame):
  antennaIsOn = [True for _ in range(20)]
  lDefaultValues = lDefaultValuesSBOSelexClearance
  rDefaultValues = rDefaultValuesSelex
  # [[1.19,3.04,5.30,7.73,10.34,13.13,16.09,19.23,22.54,26.03],
  #   [93,100,100,93,82,66,45,29,15,11],
  #   [0,0,0,0,0,0,0,0,0,0]]
  rDefaultValuesSBO = rDefaultValuesSBOSelex
  # [[1.19,3.04,5.30,7.73,10.34,13.13,16.09,19.23,22.54,26.03],
  #   [0.55,1.89,3.38,4.82,6,6.66,6.59,5.75,4.2,3.29],
  #   [0,0,0,0,0,0,0,0,0,0]]
  leftVars = [[0 for _ in range(10)] for _ in range(3)]
  leftSboVars = [[0 for _ in range(10)] for _ in range(3)]
  rightVars = [[0 for _ in range(10)] for _ in range(3)]
  rSboVars = [[0 for i in range(10)] for _ in range(3)]
  antennas = []

  def __init__(self, parent, controller):
    Frame.__init__(self, parent)
    self.controller = controller
    self.imFrame = Frame(self, height=645, width=900)
    self.controlPanel = Frame(self, bg="#3A3939", height=645, width=300)
    self.imFrame.place(x=-580, y=-685)
    self.antennaFrame = Frame(self, height=680, width=50)
    self.antennaFrame.place(x=0, y=0)
    #controlPanel.pack(side=RIGHT,fill=X)
    self.controlPanel.pack(side=RIGHT, fill=Y)
    self.controlPanel.pack_propagate(0)
    self.controlPanel.grid_propagate(0)
    self.controlPanel.grid_rowconfigure(0, minsize=50)
    self.controlPanel.grid_columnconfigure(1, weight=1)

    Label(self.controlPanel,
          text="Control Panel",
          fg="white",
          bg="#3A3939",
          font=("Ubuntu", 18, "bold")).pack(side=TOP, fill=X)
    antennaOnImage = PhotoImage(file="assets/antenna_on.png")
    antennaOffImage = PhotoImage(file="assets/antenna_off.png")
    for i in range(3):
      for j in range(10):
        self.leftVars[i][j] = DoubleVar(
          value=lDefaultValuesSelexClearance[i][j])
        self.leftSboVars[i][j] = DoubleVar(
          value=lDefaultValuesSBOSelexClearance[i][j])
        self.rightVars[i][j] = DoubleVar(
          value=rDefaultValuesSelexClearance[i][j])
        self.rSboVars[i][j] = StringVar(
          value=rDefaultValuesSBOSelexClearance[i][j])
    for i in range(len(self.antennaIsOn)):
      self.antennas.append(
        Button(self.antennaFrame,
               image=antennaOnImage,
               bd=0,
               command=lambda c=i: self.antennaCommand(c, antennaOffImage,
                                                       antennaOnImage)))
      self.antennas[i].pack(side=TOP)
    self.enableCsb = IntVar(value=1)
    Checkbutton(self.controlPanel, text="CSB",
                variable=self.enableCsb).grid(row=1, columnspan=2, pady=10)
    self.enableSbo = IntVar(value=1)
    Checkbutton(self.controlPanel, text="SBO",
                variable=self.enableSbo).grid(row=2, columnspan=2, pady=10)
    self.horizontalOrVertical = IntVar(value=1)
    Checkbutton(self.controlPanel,
                text="Horizontal/Vertical",
                variable=self.horizontalOrVertical).grid(row=3,
                                                         columnspan=2,
                                                         pady=10)
    self.clearanceOrCourse = IntVar(value=1)
    Checkbutton(self.controlPanel,
                text="Clearance/Course",
                variable=self.clearanceOrCourse).grid(row=4,
                                                      columnspan=2,
                                                      pady=10)
    self.localizerHeightVar = StringVar(value=5)
    Label(self.controlPanel,
          text="Lz Height (m)",
          bg="#3A3939",
          fg="white",
          font=("Ubuntu", 13)).grid(row=5,
                                    column=0,
                                    padx=30,
                                    pady=10,
                                    sticky=E)
    Entry(self.controlPanel,
          textvariable=self.localizerHeightVar,
          width=8,
          bg="#4a4848",
          fg="white",
          insertbackground="white").grid(row=5, column=1, sticky=W)
    param_button = Button(self.controlPanel,
                          text="Adjust antenna \n parameters",
                          padx=8,
                          pady=6,
                          cursor='hand2',
                          relief=FLAT,
                          command=self.openParametersWindow).grid(row=6,
                                                                  columnspan=2,
                                                                  pady=10)
    submit_button = Button(self.controlPanel,
                           text="Generate",
                           padx=8,
                           pady=4,
                           cursor='hand2',
                           relief=FLAT,
                           command=self.Generate).grid(row=7, columnspan=2)

  def updateCSBAndSBOVars(self):
    varsFlag = self.clearanceOrCourse.get() == 1
    lCSB = lDefaultValuesSelexClearance if varsFlag else lDefaultValuesSelex
    lSBO = lDefaultValuesSBOSelexClearance if varsFlag else lDefaultValuesSBOSelex
    rCSB = rDefaultValuesSelexClearance if varsFlag else rDefaultValuesSelex
    rSBO = rDefaultValuesSBOSelexClearance if varsFlag else rDefaultValuesSBOSelex
    for i in range(3):
      for j in range(10):
        self.leftVars[i][j] = DoubleVar(value=lCSB[i][j])
        self.leftSboVars[i][j] = DoubleVar(value=lSBO[i][j])
        self.rightVars[i][j] = DoubleVar(value=rCSB[i][j])
        self.rSboVars[i][j] = StringVar(value=rSBO[i][j])

  def plotRadiation(self, theta, Ecsb, Esbo):
    for w in self.imFrame.winfo_children():
      w.destroy()
    fig = plt.Figure(figsize=(20, 20))
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)
    ax.set_xticks(np.arange(-np.pi, np.pi, np.pi / 90))
    ax.set_thetamin(90)
    ax.set_thetamax(-90)
    if self.horizontalOrVertical.get() == 0:
      ax.vlines(0,
                0,
                max(max(Esbo), max(Ecsb)),
                colors='black',
                linestyles='solid')
    if self.enableCsb.get() == 1:
      ax.plot(theta, Ecsb)
    if self.enableSbo.get() == 1:
      ax.plot(theta, Esbo)
    canvas = FigureCanvasTkAgg(fig, self.imFrame)
    canvas.draw()
    wid = canvas.get_tk_widget()
    wid.place(x=0, y=0)
    toolbar = NavigationToolbar2Tk(canvas, self.imFrame)
    toolbar.update()
    tool = canvas.get_tk_widget()
    tool.pack(side=RIGHT)

  def openParametersWindow(self):
    self.updateCSBAndSBOVars()
    newWindow = Toplevel(bg="#3A3939")
    newWindow.title("Localizer antenna parameters")
    newWindow.geometry("600x350")
    # newWindow.grid_rowconfigure(5, minsize=10)
    newWindow.grid_rowconfigure(12, minsize=10)
    newWindow.grid_rowconfigure(20, minsize=10)
    Label(newWindow, text="Left CSB", bg="#3A3939", fg="white").grid(row=0,
                                                                     column=0)
    Label(newWindow, text="Distance", bg="#3A3939", fg="white").grid(row=1,
                                                                     column=0)
    Label(newWindow, text="Amplitude", bg="#3A3939", fg="white").grid(row=2,
                                                                      column=0)
    Label(newWindow, text="Phase", bg="#3A3939", fg="white").grid(row=3,
                                                                  column=0)
    for i in range(10):
      Label(newWindow, text="L" + str(i + 1), bg="#3A3939",
            fg="white").grid(row=0, column=i + 1)
    for i in range(3):
      for j in range(10):
        Entry(newWindow,
              textvariable=self.leftVars[i][j],
              width=8,
              bg="#4a4848",
              fg="white",
              insertbackground="white").grid(row=i + 1, column=j + 1)

    Label(newWindow, text="Left SBO", bg="#3A3939", fg="white").grid(row=7,
                                                                     column=0)
    Label(newWindow, text="Distance", bg="#3A3939", fg="white").grid(row=8,
                                                                     column=0)
    Label(newWindow, text="Amplitude", bg="#3A3939", fg="white").grid(row=9,
                                                                      column=0)
    Label(newWindow, text="Phase", bg="#3A3939", fg="white").grid(row=10,
                                                                  column=0)
    for i in range(10):
      Label(newWindow, text="L" + str(i + 1), bg="#3A3939",
            fg="white").grid(row=7, column=i + 1)
    for i in range(3):
      for j in range(10):
        Entry(newWindow,
              textvariable=self.leftSboVars[i][j],
              width=8,
              bg="#4a4848",
              fg="white",
              insertbackground="white").grid(row=i + 8, column=j + 1)

    Label(newWindow, text="Right CSB", bg="#3A3939", fg="white").grid(row=24,
                                                                      column=0)
    Label(newWindow, text="Distance", bg="#3A3939", fg="white").grid(row=25,
                                                                     column=0)
    Label(newWindow, text="Amplitude", bg="#3A3939", fg="white").grid(row=26,
                                                                      column=0)
    Label(newWindow, text="Phase", bg="#3A3939", fg="white").grid(row=27,
                                                                  column=0)
    for i in range(10):
      Label(newWindow, text="R" + str(i + 1), bg="#3A3939",
            fg="white").grid(row=24, column=i + 1)
    for i in range(3):
      for j in range(10):
        Entry(newWindow,
              textvariable=self.rightVars[i][j],
              width=8,
              bg="#4a4848",
              fg="white",
              insertbackground="white").grid(row=i + 25, column=j + 1)

    Label(newWindow, text="Right SBO", bg="#3A3939", fg="white").grid(row=36,
                                                                      column=0)
    Label(newWindow, text="Distance", bg="#3A3939", fg="white").grid(row=37,
                                                                     column=0)
    Label(newWindow, text="Amplitude", bg="#3A3939", fg="white").grid(row=38,
                                                                      column=0)
    Label(newWindow, text="Phase", bg="#3A3939", fg="white").grid(row=39,
                                                                  column=0)
    for i in range(10):
      Label(newWindow, text="R" + str(i + 1), bg="#3A3939",
            fg="white").grid(row=36, column=i + 1)
    for i in range(3):
      for j in range(10):
        Entry(newWindow,
              textvariable=self.rSboVars[i][j],
              width=8,
              bg="#4a4848",
              fg="white",
              insertbackground="white").grid(row=i + 37, column=j + 1)

  def fTheta(self, t):
    return pow(
      10, -(0.0000442 * pow(abs(t), 3) + 0.0023678 * pow(abs(t), 2) +
            0.016252 * abs(t)) / 20)

  def Generate(self):
    self.updateCSBAndSBOVars()
    height = float(self.localizerHeightVar.get())
    theta = np.arange(
      -np.pi / 2, np.pi /
      2, 0.005) if self.horizontalOrVertical.get() == 1 else np.arange(
        0, np.pi / 2, 0.005)
    Ecsb = 0 * theta
    Esbo = 0 * theta
    # Frp = 0*theta
    # Rp,Th,Phi = 4260,2,0
    if self.horizontalOrVertical.get() == 1:
      for i in range(10):
        if self.antennaIsOn[10 + i]:
          lDist, lAmp, lPhase = float(self.leftVars[0][i].get()), float(
            self.leftVars[1][i].get()), np.radians(
              float(self.leftVars[2][i].get()))
          rDist, rAmp, rPhase = float(self.rightVars[0][i].get()), float(
            self.rightVars[1][i].get()), np.radians(
              float(self.rightVars[2][i].get()))
          lSboDist, lSboAmp, lSboPhase = float(
            self.leftSboVars[0][i].get()), float(
              self.leftSboVars[1][i].get()), np.radians(
                float(self.leftSboVars[2][i].get()))
          rSboDist, rSboAmp, rSboPhase = float(
            self.rSboVars[0][i].get()), float(
              self.rSboVars[1][i].get()), np.radians(
                float(self.rSboVars[2][i].get()))

          Ecsb += lAmp * (np.cos(
            (2 / 2.72) * lDist * np.pi * np.sin(theta + lPhase)
          )) * self.fTheta(theta + lPhase) + rAmp * (np.cos(
            (2 / 2.72) * rDist * np.pi *
            np.sin(theta + rPhase))) * self.fTheta(theta + rPhase)

          Esbo += lSboAmp * self.fTheta(theta + lSboPhase) * ((np.sin(
            (2 / 2.72) * lSboDist * np.pi * np.sin(theta + lSboPhase)
          ))) + rSboAmp * self.fTheta(theta + rSboPhase) * ((np.sin(
            (2 / 2.72) * rSboDist * np.pi * np.sin(theta + rSboPhase))))
    else:
      for i in range(10):
        if self.antennaIsOn[10 + i]:
          amp, phase = float(self.rightVars[1][i].get()), np.radians(
            float(self.rightVars[2][i].get()))
          sboAmp, sboPhase = float(self.rSboVars[1][i].get()), np.radians(
            float(self.rSboVars[2][i].get()))
          Ecsb += 2 * amp * (np.sin(
            (1 / 2.72) * height * np.pi *
            np.sin(theta + phase))) * self.fTheta(theta + phase)
          Esbo += 2 * sboAmp * (np.sin(
            (1 / 2.72) * height * np.pi *
            np.sin(theta + sboPhase))) * self.fTheta(theta + sboPhase)
    Esbo = abs(Esbo)
    Ecsb = abs(Ecsb)
    self.plotRadiation(theta, Ecsb, Esbo)

  def antennaCommand(self, i, antennaOffImage, antennaOnImage):
    j = len(self.antennaIsOn) - i - 1
    if self.antennaIsOn[i]:
      self.antennas[i].config(image=antennaOffImage)
      self.antennas[j].config(image=antennaOffImage)
    else:
      self.antennas[i].config(image=antennaOnImage)
      self.antennas[j].config(image=antennaOnImage)
    self.antennaIsOn[i] = not self.antennaIsOn[i]
    self.antennaIsOn[j] = not self.antennaIsOn[j]
