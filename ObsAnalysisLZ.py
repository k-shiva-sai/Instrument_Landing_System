from tkinter import *
from turtle import color
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)


class ObsAnalysisLZ(Frame):

  def __init__(self, parent, controller):
    Frame.__init__(self, parent)
    self.controller = controller
    self.imFrame = Frame(self, height=560, width=900)
    self.labelFrame = Frame(self, height=85, width=900)
    self.frenselLabel = Label(self.labelFrame, text="", font=("Ubuntu", 15))
    self.electricFieldLabel = Label(self.labelFrame,
                                    text="",
                                    font=("Ubuntu", 15))
    self.controlPanel = Frame(self, bg="#3A3939", height=680, width=300)
    self.imFrame.pack(side=LEFT, fill=Y)
    self.labelFrame.place(x=0, y=590)
    self.frenselLabel.grid(row=0, column=0)
    self.electricFieldLabel.grid(row=1, column=0)
    #controlPanel.pack(side=RIGHT,fill=X)
    self.controlPanel.pack(side=RIGHT, fill=Y)
    self.controlPanel.pack_propagate(0)
    self.controlPanel.grid_propagate(0)
    self.controlPanel.grid_rowconfigure(0, minsize=50)
    Label(self.controlPanel,
          text="Control Panel",
          fg="white",
          bg="#3A3939",
          font=("Ubuntu", 18, "bold")).pack(side=TOP, fill=X)
    self.labelList = [
      "Carrier Frequency (MHz)", "Lz to Obs Distance (m)",
      "Lz to Plane Distance (m)", "Localizer Height (m)",
      "Aircraft altitude (m)", "Obstacle Height (m)", "Power i/p (w)",
      "Transmitter Gain"
    ]
    defaultValues = [110, 12000, 33300, 3100, 4900, 4096, 15, 1]
    self.labelWidgets(self.controlPanel, self.labelList)
    var = {}
    for i in range(len(self.labelList)):
      var[self.labelList[i]] = StringVar(value=defaultValues[i])

    for i in range(len(self.labelList)):
      Entry(self.controlPanel,
            textvariable=var[self.labelList[i]],
            font=("Ubuntu", 12),
            width=8,
            bg="#4a4848",
            fg="white",
            insertbackground="white").grid(row=i + 1, column=1, padx=5, pady=6)

    submit_button = Button(self.controlPanel,
                           text="Generate",
                           padx=8,
                           pady=4,
                           cursor='hand2',
                           relief=FLAT,
                           command=lambda: self.Generate(var)).grid(row=14,
                                                                    column=1)

  def plot(self, vi, Ldiff, v, loss, electricFeild, dist):
    for w in self.imFrame.winfo_children():
      w.destroy()
    fig = plt.Figure(dpi=115)
    pltLoss = fig.add_subplot(111,
                              title="Frensels kirchoffs diffraction",
                              xlabel="Vi",
                              ylabel="Ldiff")
    pltLoss.axvline(v, color='r', linestyle='--')
    pltLoss.axhline(loss, color='r', linestyle='--')
    # pltElectricFeild = fig.add_subplot(212,xlabel='Distance (km)',ylabel='Electric feild (μv/m)')
    # pltElectricFeild.plot(dist,electricFeild)
    # fig.tight_layout()
    pltLoss.grid()
    # pltSbo.set_yticks(np.arange(-25,6,5))
    # pltSbo.set_xticks(np.arange(-5,5.1,1))
    pltLoss.plot(vi, Ldiff)
    # fig.savefig('out.jpg')
    # canvas = Canvas(imFrame,width=999,height=999)
    # canvas.pack()
    # pilImage = Image.open("out.jpg")
    # image = ImageTk.PhotoImage(pilImage)
    # canvas.create_image(400,400,image=image)
    canvas = FigureCanvasTkAgg(fig, self.imFrame)
    canvas.draw()
    wid = canvas.get_tk_widget()
    wid.place(x=0, y=0)
    toolbar = NavigationToolbar2Tk(canvas, self.imFrame)
    toolbar.update()
    tool = canvas.get_tk_widget()
    tool.pack(side=BOTTOM)

    # 1. calculate 1st frensels zone radius
    # 2. calculate clearance
    # 3. cal knife edge prop factor Vi
    #  i. cal normalize electric field
    #  ii. cal path loss Ldiff
    # 4. plot Ldiff vs Vi

  def cal_Loss(vi):
    if vi < -1:
      return 0
    elif vi <= 0:
      return 20 * np.log10(0.5 - 0.62 * vi)
    elif vi <= 1:
      return 20 * np.log10(0.5 * np.exp(-0.95 * vi))
    elif vi <= 2.4:
      return 20 * np.log10(0.4 - np.sqrt(0.1184 - (0.38 - 0.1 * vi)**2))
    else:
      return 20 * np.log10(0.225 / vi)

  def cal_LossP(v):
    vec = np.arange(v, v + 100.01, 0.01)
    F = ((1 + 1j) / 2) * np.sum(np.exp((-1j) * np.pi * (vec**2) / 2))
    return np.log10(abs(F))

  def Generate(self, var):
    Fc = float(var[self.labelList[0]].get()) * 10**6
    d1 = float(var[self.labelList[1]].get())
    d = float(var[self.labelList[2]].get())
    Ht = float(var[self.labelList[3]].get())
    Hr = float(var[self.labelList[4]].get())
    hobs = float(var[self.labelList[5]].get())
    powerInp = float(var[self.labelList[6]].get())
    ge = float(var[self.labelList[7]].get())
    lamda = (3 * (10**8)) / Fc
    Ae = 8493333  #aperture of earth
    d2 = d - d1
    ht = Ht - (d1**2) / (2 * Ae)
    hr = Hr - (d2**2) / (2 * Ae)
    print(ht, hr, "h")
    Eo = (
      (10**6) *
      (30 * powerInp * ge)**0.5) / d  #Electric field intensity in free space
    rd = (d**2 + (hr - ht)**2)**0.5
    rr = (d**2 + (hr + ht)**2)**0.5
    deltaPhi = -(rr - rd) * (2 * np.pi / lamda)
    sigh = np.arctan((ht + hr) / (d))
    r = np.sqrt((lamda * d1 * d2) / (d))
    c = ((ht - hobs) * d2 + (hr - hobs) * d1) / (d)
    print(ht, hr, hobs, d1, d2, d)
    eo = 8.854 * 10**(-12)
    es = 15 * 8.854 * 10**(-12)  #Es = Er*Eo permeability
    #es = es - (1j)*(5*10**(-12))/(2*np.pi*110)
    n = np.sqrt(es / eo)
    rho = (np.sin(sigh) -
           (n**2 - np.cos(sigh))**0.5) / (np.sin(sigh) +
                                          (n**2 - np.cos(sigh))**0.5)
    div = (1 + 2 * d1 * d2 / (Ae * d * np.sin(sigh)))**-0.5
    Ed = 0
    print(c, r, "out")
    if c <= r:
      self.frenselLabel.config(text="Obstacle falls in 1st fresnel zone")
    else:
      self.frenselLabel.config(text="Obstacle is not in 1st fresnel zone")
    v = c * np.sqrt(
      (2 * d) / (lamda * d1 * d2))  #np.sqrt((2 * d) / (lamda * d1 * d2) * c)
    vN = c * np.sqrt((2 * d) / (lamda * d1 * d2))
    lossN = 6.9 + 20 * np.log10(np.sqrt((vN - 0.1)**2 + 1) + vN - 0.1)
    print(lamda, "lambda")
    print(v, vN, lossN, "V")
    vi = np.arange(-5, 5.001, 0.01)
    F = np.zeros(len(vi), dtype="complex")
    for n in range(0, len(vi)):
      vec = np.arange(vi[n], vi[n] + 100.01, 0.01)
      F[n] = ((1 + 1j) / 2) * np.sum(np.exp((-1j) * np.pi * (vec**2) / 2))
    F = abs(F) / abs(F[0])
    loss = 0
    for i in range(len(vi)):
      if abs(-0.49 - vi[i]) < 0.001:
        print("{0:.1f} db {1:.2f}m".format(20 * np.log10(F[i]), vi[i]))
      if abs(-0.56 - vi[i]) < 0.001:
        print("{0:.2f} db {1:.2f}m".format(20 * np.log10(F[i]), vi[i]))
      if abs(-v - vi[i]) < 0.005:
        loss = F[i]
        print("{0:.2f} db {1:.2f}m".format(20 * np.log10(F[i]), vi[i]))

    # if loss is not None:
    #   self.electricFieldLabel.config(
    #     text="Electric feild is {0:.3f}. Loss is {1:.4f}%. Ideal Eo is {2:.4f}."
    #     .format(Eo * loss, (1 - loss) * 100, Eo))
    # else:
    #   self.electricFieldLabel.config(
    #     text=
    #     "Unable to calculate electric feild. Knife edge value is out of range")
    self.electricFieldLabel.config(
      text="Ideal Eo is {0:.4f}. Loss is {1:.4f} db. ".format(Eo, lossN))
    #print(div,deltaPhi,Eo)

    dist = np.arange(0.01, 46, 0.01)
    electricFeild = (np.sqrt(30 * powerInp * 1)) / dist
    electricFeild[0] = 0
    res = (np.sqrt(30 * powerInp * 1)) / d
    E = res * (1 + abs(rho) * div * np.exp(1j * deltaPhi))
    self.plot(vi, 20 * np.log10(F)[::-1], v, 20 * np.log10(loss),
              electricFeild, dist)
    print(rho, div, sigh, deltaPhi, res)
    print(E * (10**6), res, np.exp(1j * deltaPhi))

    #menu bar
    # menuFontStyle = ('Roboto',10,'bold')
    # file = Label(top,text="File",bg="#9C4242",fg="white",font=menuFontStyle)
    # file.pack(side=LEFT,padx=6,pady=2)
    # menu = Label(top,text="Menu",bg="#9C4242",fg="white",font=menuFontStyle)
    # menu.pack(side=LEFT,padx=6,pady=2)
    # help = Label(top,text="Help",bg="#9C4242",fg="white",font=menuFontStyle)
    # help.pack(side=LEFT,padx=6,pady=2)

    #control panel
  def labelWidgets(self, root, labelList):
    for i in range(len(labelList)):
      Label(root,
            text=labelList[i],
            bg="#3A3939",
            fg="white",
            font=("Ubuntu", 13)).grid(row=i + 1, padx=5, pady=6)
