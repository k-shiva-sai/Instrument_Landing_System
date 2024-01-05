from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image,ImageTk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)

def donothing():
  pass

root = Tk()
root.geometry("1200x680")
root.title("ILS Simulator")
root.iconphoto(False,PhotoImage(file="assets/flight.png"))
top = Frame(bg="#9C4242",height=35,width=1200)
imFrame = Frame(height=645,width=900)
imFrame.place(x=0,y=35)
top.pack(side=TOP,fill=X)
controlPanel = Frame(bg="#3A3939",height=680,width=300)
controlPanel.pack(side=RIGHT,fill=X)
controlPanel.pack_propagate(0)
controlPanel.grid_propagate(0)
top.pack_propagate(0)
controlPanelTitle = Label(controlPanel,text="Control Panel",fg="white",bg="#3A3939",font=("Ubuntu",18,"bold"))
controlPanelTitle.pack(side=TOP,padx=10,pady=10)

def plot(vi,Ldiff):
  for w in imFrame.winfo_children():
    w.destroy()
  fig = plt.Figure(dpi=125)
  pltSbo = fig.add_subplot(111,title="Frensels kirchoffs diffraction",xlabel="Vi",ylabel="Ldiff")
  fig.tight_layout()
  pltSbo.grid()
  # pltSbo.set_yticks(np.arange(-25,6,5))
  # pltSbo.set_xticks(np.arange(-5,5.1,1))
  pltSbo.plot(vi,Ldiff)
  # fig.savefig('out.jpg')
  # canvas = Canvas(imFrame,width=999,height=999)
  # canvas.pack()
  # pilImage = Image.open("out.jpg")
  # image = ImageTk.PhotoImage(pilImage)
  # canvas.create_image(400,400,image=image)
  canvas = FigureCanvasTkAgg(fig,imFrame)
  canvas.draw()
  wid = canvas.get_tk_widget()
  wid.place(x=0,y=0)
  toolbar = NavigationToolbar2Tk(canvas,imFrame)
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
    elif vi<=0:
        return 20*np.log10(0.5 - 0.62*vi)
    elif vi<=1:
        return 20*np.log10(0.5*np.exp(-0.95*vi))
    elif vi<=2.4:
        return 20*np.log10(0.4 - np.sqrt(0.1184-(0.38-0.1*vi)**2))
    else:
        return 20*np.log10(0.225/vi)

def cal_LossP(v):
  vec = np.arange(v,v+100.01,0.01)
  F = ((1 + 1j)/2)*np.sum(np.exp((-1j)*np.pi*(vec**2)/2))
  return np.log10(abs(F))

def Generate(var):
    Fc = float(var["Fc (MHz)"].get())*10**6
    d1 = float(var["d1"].get())
    d2 = float(var["d2"].get())
    Ht = float(var["Ht"].get())
    Hr = float(var["Hr"].get())
    hobs = float(var["Hobs"].get())
    powerInp = float(var["Power i/p"].get())
    lamda = (3*(10**8))/Fc
    Ae = 8493333            #aperture of earth
    ht = Ht - (d1**2) / (2*Ae)
    hr = Hr - (d2**2) / (2*Ae)
    print(ht,hr,"h")
    d = d1+d2
    Eo = ((10**6)*(30*powerInp*1)**0.5)/d  #Electric field intensity in free space uv/m
    rd = (d**2 + (hr-ht)**2)**0.5
    rr = (d**2 + (hr+ht)**2)**0.5
    deltaPhi = (rr-rd)*(2*np.pi/lamda)
    sigh = np.arctan((ht+hr)/(d))
    r = np.sqrt((lamda*d1*d2)/(d))
    c = ((ht - hobs)*d2 + (hr - hobs)*d1)/(d)
    eo = 8.854*10**(-12)
    es = 15*8.854*10**(-12) #Es = Er*Eo permeability
    es = es - (1j)*(5*10**(-12))/(2*np.pi*110)
    n = np.sqrt(es/eo)
    rho = (np.sin(sigh)-(n**2 - np.cos(sigh))**0.5)/(np.sin(sigh)+(n**2 - np.cos(sigh))**0.5)
    div = (1 + 2*d1*d2/(Ae*d*np.sin(sigh)))**-0.5
    Ed = 0
    print(c,r,"out")
    if c<=r:
        print("Obstacle falls in 1st fresnel zone")
    else:
        print("Obstacle is not in 1st fresnel zone")
    v = np.sqrt((2*d)/(lamda*d1*d2))*c
    print(v," dfghfg")
    vi = np.arange(-5,5.001,0.01)
    F = np.zeros(len(vi),dtype="complex")
    for n in range(0,len(vi)):
      vec = np.arange(vi[n],vi[n]+100.01,0.01)
      F[n] = ((1 + 1j)/2)*np.sum(np.exp((-1j)*np.pi*(vec**2)/2))
    F = abs(F)/abs(F[0])
    loss = None
    for i in range(len(vi)):
      if abs(-0.49-vi[i])<0.001:
        print("{0:.1f} db {1:.2f}m".format(20*np.log10(F[i]),vi[i]))
      if abs(-0.56-vi[i])<0.001:
        print("{0:.2f} db {1:.2f}m".format(20*np.log10(F[i]),vi[i]))
      if abs(-v-vi[i])<0.01:
        loss = F[i]
        print("{0:.2f} db {1:.2f}m".format(20*np.log10(F[i]),vi[i]))
    if loss is not None:
      print("Electric feild is {0:.3f}. Loss is {1:.4f}. Ideal Eo is {2:.4f}".format(Eo*loss,loss,Eo))
    else:
      print("Unable to calculate electric feild. Knife edge value is out of range")
    #print(div,deltaPhi,Eo)

    dist = np.arange(40,46,0.001)
    res = ((np.sqrt(30*powerInp*1))*(10**6))/(dist*1000)
    E = res*(1 + rho*div*np.exp(-1j*deltaPhi))
    plot(vi,20*np.log10(F)[::-1])

    #plot(vi,20*np.log10(F))

#menu bar
menuFontStyle = ('Roboto',10,'bold')
file = Label(top,text="File",bg="#9C4242",fg="white",font=menuFontStyle)
file.pack(side=LEFT,padx=6,pady=2)
menu = Label(top,text="Menu",bg="#9C4242",fg="white",font=menuFontStyle)
menu.pack(side=LEFT,padx=6,pady=2)
help = Label(top,text="Help",bg="#9C4242",fg="white",font=menuFontStyle)
help.pack(side=LEFT,padx=6,pady=2)

#control panel
def labelWidgets(root,labelList):
  for i in range(len(labelList)):
    Label(root,text=labelList[i],bg="#3A3939",fg="white",font=("Ubuntu",15)).grid(row=i+1,padx=20,pady=6)

controlPanel.grid_rowconfigure(0,minsize=50)
labelList = ["Fc (MHz)","d1","d2","Ht","Hr","Hobs","Power i/p"]
defaultValues = [110,6470,39830,3,2623,20,15]
labelWidgets(controlPanel,labelList)
var = {}
for i in range(len(labelList)):
  var[labelList[i]] = StringVar(value=defaultValues[i])

for i in range(len(labelList)):
  Entry(controlPanel,textvariable=var[labelList[i]],font=("Ubuntu",12),width=12,
  bg="#4a4848",fg="white",insertbackground="white").grid(row=i+1,column=1,padx=20,pady=6)

submit_button = Button(controlPanel,text = "Generate",padx=8,pady=4,cursor='hand2', relief=FLAT,
  command=lambda: Generate(var)).grid(row=14,column=1)

root.mainloop()