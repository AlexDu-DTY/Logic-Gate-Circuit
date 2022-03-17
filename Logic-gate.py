####################################
#andrew id: tianyuad
#name: Alex Du
#Section: B
####################################

####################################
# draw gates
####################################
class Gate(object):
    #initialization
    def __init__(self):
        self.inputGates=[]
        self.outputGates=[]
        self.inputVals=None
        self.inputValues = []
        self.outputValue=None
        self.maxInputGates=1
        self.transform()
    #create the list of inputValues
    def transform(self):
        if(self.inputVals == None):
            return []
        self.inputValues = []
        for (key,val) in self.inputVals.items():
            if((key,val) in self.inputValues):
                continue
            self.inputValues += [(key,val)]
            
        pass
    #connect two gates
    def connectTo(self,gate):
        if(len(gate.inputGates) < gate.maxInputGates):
            if gate not in self.outputGates: 
                self.outputGates.append(gate)
            if self not in gate.inputGates: 
                gate.inputGates.append(self)
            if gate.inputVals == None: gate.inputVals = dict()
            gate.inputVals[self] = self.outputValue
            if type(self) == Output:
                pass
        self.transform()
    #use input to decide output
    def inputToOutput(self):
        if self.inputVals!=None:
            self.outputValue=False
        elif self.inputVals==None:
            self.outputValue=None
            return
        if type(self) == Or: self.orGate()
        elif type(self) == And: self.andGate()            
        elif type(self) == Not:
            for key in self.inputVals:
                self.outputValue = not self.inputVals[key]
        elif type(self) == Output or type(self) == Input: 
            for key in self.inputVals:
                self.outputValue = self.inputVals[key]
        self.transform()
        return
    #Or type helper function
    def orGate(self):
        if len(self.inputVals)==2:
            for key in self.inputVals:
                if self.inputVals[key]==True:
                    self.outputValue=True
                    break
            #None type is more priviledged than all types
            for key in self.inputVals:
                if self.inputVals[key] == None:
                    self.outputValue = None
                    return
        else:
            self.outputValue=None
        self.transform()
    #And type helper function
    def andGate(self):
        if len(self.inputVals)==2:
            for key in self.inputVals:
                if self.inputVals[key]==True: self.outputValue=True
                else:
                    self.outputValue=False
                    break
            for key in self.inputVals:
                if self.inputVals[key] == None:
                    self.outputValue = None
                    return
        else: self.outputValue=None
        self.transform()
    #set the input values
    def setInputValue(self,gate,TorF):
        try:
            if self.inputVals==None:
                self.inputVals=dict()
            self.inputVals[gate]=TorF
            self.inputToOutput()#generate its output
            for index in range(len(self.outputGates)):
                self.outputGates[index].setInputValue(self,self.outputValue)
        
            self.transform()
        except: return
    #return inputgates
    def getInputGates(self):
        self.transform()
        return self.inputGates
    #return maximum numbers of inputgates
    def getMaxInputGates(self):
        self.transform()
        return self.maxInputGates
    #return outputgates
    def getOutputGates(self):
        self.transform()
        return self.outputGates

class Input(Gate):
    #initialization
    def __init__(self):
        self.inputGates=[]
        self.outputGates=[]
        self.inputVals=None
        self.outputValue=None
        self.inputValues = []
        self.maxInputGates=0
        self.transform()

class Output(Gate):
    #all covered in Gate class
    pass

class And(Gate):
    #initialization
    def __init__(self):
        self.inputGates=[]
        self.outputGates=[]
        self.inputVals=None
        self.outputValue=None
        self.inputValues = []
        self.maxInputGates=2
        self.transform()

class Or(Gate):
    #initialization
    def __init__(self):
        self.inputGates=[]
        self.outputGates=[]
        self.inputVals=None
        self.outputValue=None
        self.inputValues = []
        self.maxInputGates=2
        self.transform()

class Not(Gate):
    #initialization
    def __init__(self):
        self.inputGates=[]
        self.outputGates=[]
        self.inputVals=None
        self.outputValue=None
        self.inputValues = []
        self.maxInputGates=1
        self.transform()


######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################

def testGateClass0_basics():
    gate1 = Gate()
    gate2 = Gate()
    assert(gate1.getInputGates() == [])
    assert(gate1.getOutputGates() == [])

    assert(gate1.inputValues == [ ])
    assert(gate1.outputValue == None)

    # you can connect gates to each other! 
    gate1.connectTo(gate2)
    assert(gate1.getOutputGates() == [gate2])
    assert(gate2.getInputGates() == [gate1])

    # gate2 now has gate1 as an input, but since gate1.outputValue = None,
    #assert(gate2.inputValues == [(gate1,None)])
    assert(gate2.inputValues == [(gate1, None)])

def testGateClass1_inputToOutput():
    # Connect an input gate to an output gate
    in1 = Input()
    out1 = Output()
    in1.connectTo(out1)

    assert(in1.getInputGates() == [ ])
    assert(in1.getMaxInputGates() == 0) # an input gate can't have any inputs
    assert(in1.getOutputGates() == [ out1 ])
    assert(out1.getInputGates() == [ in1 ])
    assert(out1.getMaxInputGates() == 1)
    assert(out1.getOutputGates() == [ ])

    assert(in1.inputValues == [ ])
    assert(in1.outputValue == None)
    
    #assert(out1.inputValues == [(in1, None)])
    assert(out1.outputValue == None)

    in2 = Input()
    in2.connectTo(out1)
    # since out1 has a maximum of one input, and it already has in1 as an input,
    # this shouldn't do anything!
    assert(in2.getOutputGates() == [])
    assert(out1.getInputGates() == [ in1 ])

    # setInputValue should take in two values - a fromGate and a value, which
    # represent the gate the input is coming from, and the value of that gate.
    # Here, in1 is an input gate, meaning that it's input isn't coming from
    # anywhere! So, the fromGate = None, and the value = True in this case.

    # be careful to examine the test cases to figure out what happens to the
    # gates you're connected to once you set the input value!
    in1.setInputValue(None, True)
    print(in1.inputVals=={None:True})
    assert(in1.inputValues == [(None,True)])
    assert(in1.outputValue == True)
    assert(out1.inputValues == [(in1,True)])
    assert(out1.outputValue == True)
    # and set the input to False
    in1.setInputValue(None, False)
    assert(in1.inputValues == [(None,False)])
    assert(in1.outputValue == False)
    assert(out1.inputValues == [(in1,False)])
    assert(out1.outputValue == False)

def testGateClass2_oneNotGate():
    in1 = Input()
    out1 = Output()
    not1 = Not()
    in1.connectTo(not1)
    not1.connectTo(out1)

    assert(in1.outputValue == not1.outputValue == out1.outputValue == None)

    in1.setInputValue(None, False)
    assert(not1.inputValues == [(in1,False)])
    assert(out1.inputValues == [(not1,True)])
    assert(out1.outputValue == True)

    in1.setInputValue(None, True)
    assert(not1.inputValues == [(in1,True)])
    assert(out1.inputValues == [(not1,False)])
    assert(out1.outputValue == False)

def testGateClass3_oneAndGate():
    in1 = Input()
    in2 = Input()
    out1 = Output()
    and1 = And()
    in1.connectTo(and1)
    in2.connectTo(and1)
    and1.connectTo(out1)
    assert(out1.outputValue == None)
    in1.setInputValue(None, False)
    #assert(and1.inputValues == [(in1,False)])#
    assert(and1.outputValue == None) # not ready, need both inputs
    in2.setInputValue(None, False)
    assert(and1.inputValues == [(in1,False), (in2,False)])
    assert(and1.outputValue == False)
    assert(out1.outputValue == False)

    in1.setInputValue(None, True)
    assert(and1.inputValues == [(in1,True), (in2,False)])
    assert(out1.outputValue == False)

    in2.setInputValue(None, True)
    assert(and1.inputValues == [(in1,True), (in2,True)])
    assert(out1.outputValue == True)

def testGateClass4_oneOrGate():
    in1 = Input()
    in2 = Input()
    out1 = Output()
    or1 = Or()
    in1.connectTo(or1)
    in2.connectTo(or1)
    or1.connectTo(out1)

    assert(or1.inputValues == [(in1,None), (in2,None)])
    assert(or1.outputValue == None)
    assert(out1.outputValue == None)
    in1.setInputValue(None, False)
    assert(or1.inputValues == [(in1,False), (in2,None)])
    assert(or1.outputValue == None) # not ready, need both inputs
    in2.setInputValue(None, False)
    assert(or1.inputValues == [(in1,False), (in2,False)] )
    assert(or1.outputValue == False)
    assert(out1.outputValue == False)

    in1.setInputValue(None, True)
    assert(or1.inputValues == [(in1,True), (in2,False)])
    assert(out1.outputValue == True)

    in2.setInputValue(None, True)
    assert(or1.inputValues == [(in1,True), (in2,True)])
    assert(out1.outputValue == True)

def testGateClass5_xor():
    in1 = Input()
    in2 = Input()
    out1 = Output()
    and1 = And()
    and2 = And()
    not1 = Not()
    not2 = Not()
    or1 = Or()
    in1.connectTo(and1)
    in1.connectTo(not1)
    in2.connectTo(and2)
    in2.connectTo(not2)
    not1.connectTo(and2)
    not2.connectTo(and1)
    and1.connectTo(or1)
    and2.connectTo(or1)
    or1.connectTo(out1)

    in1.setInputValue(None, False)
    in2.setInputValue(None, False)
    assert(out1.outputValue == False)

    in1.setInputValue(None, True)
    in2.setInputValue(None, False)
    assert(out1.outputValue == True)

    in1.setInputValue(None, False)
    in2.setInputValue(None, True)
    assert(out1.outputValue == True)

    in1.setInputValue(None, True)
    in2.setInputValue(None, True)
    assert(out1.outputValue == False)

def testGateClass():
    print("Testing Gate class... ", end="")
    testRTP()
    testGateClass0_basics()
    testGateClass1_inputToOutput()
    testGateClass2_oneNotGate()
    testGateClass3_oneAndGate()
    testGateClass4_oneOrGate()
    testGateClass5_xor()
    print("Passed!")

testGateClass()

from tkinter import *
#initialization
def init(data):
    data.buttonDict=dict()
    data.button=None
    data.r=5 #r for radius, simplified
    data.unit=10
    data.input=0
    data.errorBound=10
    data.threadResidue=6
    data.inpointList=[]
    data.outpointList=[]
    data.lineList=[]
    data.connectLine=[]
    data.inputButtons=[]
    data.power=False
    data.save=False
    data.path="circuit.txt"
    data.contents=""
    data.read=""
    data.location=[]
    data.gate=[]
#draw the Gate
def drawGate(canvas,data):#draw gates based on their names
    d,r,l=data.unit, data.r, data.threadResidue
    for key in data.buttonDict:
        for i in range(len(data.buttonDict[key])):
            x=int(data.buttonDict[key][i][0])
            y=int(data.buttonDict[key][i][1])
            if key=="input":
                canvas.create_oval(x-r,y-r,x+r,y+r,fill="black",outline="red")
                canvas.create_line(x+r,y,x+r+l,y,fill="red")
            elif key=="output":
                canvas.create_oval(x-r,y-r,x+r,y+r,fill="black",outline="green")
                canvas.create_line(x-r-l,y,x-r,y,fill="green")
            elif key=="and":
                canvas.create_rectangle(x-d,y-d,x+d,y+d,fill="white")
                canvas.create_oval(x,y-d,x+2*d,y+d,fill="white")
                canvas.create_rectangle(x-d+1,y-d+1,x+d-1,y+d-1,fill="white",
                    outline="white")
                canvas.create_line(x-d-l,y-d+r,x-d,y-d+r, fill="green")
                canvas.create_line(x-d-l,y+d-r,x-d,y+d-r, fill="green")
                canvas.create_line(x+2*d,y,x+2*d+l,y,fill="red")
#draw the other gate
def drawGateAdd(canvas,data):
    d,r,l=data.unit, data.r, data.threadResidue
    for key in data.buttonDict:
        for i in range(len(data.buttonDict[key])):
            x=int(data.buttonDict[key][i][0])
            y=int(data.buttonDict[key][i][1])
            if key=="or":
                 canvas.create_polygon(x-d-r,y-d,x-d-r+l/2,y-d+l,x-d-r+l/2,
            y+d-l,x-d-r,y+d,x,y+d, x+d+r,y,x,y-d,fill="white",outline="black")
                 canvas.create_line(x-d-r-l/2,y-d+l,x-d-r+l/2,y-d+l,
                    fill="green")
                 canvas.create_line(x-d-r-l/2,y+d-l,x-d-r+l/2,y+d-l, 
                    fill="green")
                 canvas.create_line(x+d+r,y,x+d+r+l,y, fill="red")
            elif key=="not":
                canvas.create_line(x-l-d,y,x+d+2*r,y)
                canvas.create_polygon(x-d,y-d/2,x-d,y+d/2,x+d,y,fill="white",
                    outline="black")
                canvas.create_oval(x+d,y-2,x+d+r-1,y+2,fill="white",
                    outline="black")

#draw the power input session
def drawPowerInput(canvas,data):
    #change the color of the input button when it has power
    for index in range(len(data.inputButtons)):
        if data.inputButtons[index][2].outputValue==True:
            x=int(data.inputButtons[index][0])
            y=int(data.inputButtons[index][1])
            r=data.r
            canvas.create_oval(x-r,y-r,x+r,y+r,fill="red",width=0)

#draw the power lines
def drawPowerLine(canvas,data):
    for index in range(len(data.lineList)):
        xL=int(data.lineList[index][0][0])
        yL=int(data.lineList[index][0][1])
        xR=int(data.lineList[index][1][0])
        yR=int(data.lineList[index][1][1])
        if data.lineList[index][0][2].outputValue==True:
            canvas.create_line(xL,yL,xR,yR,fill="red")
        else:
            canvas.create_line(xL,yL,xR,yR,fill="black")


#draw top buttons and left buttons (And)
def drawButtonAnd(canvas,data):
    r,l=data.r,data.threadResidue
    a,b,c,d,e=50,100,200,data.unit,data.r
    for index in range(1,r+1):
        canvas.create_rectangle(index*b,0,(index+1)*b,b,fill="white")
    drawSave(canvas,data)
    if data.power==True:
        canvas.create_rectangle(2*c+e,e,2*c+b-e,b-e,outline="gray",width=d)
    canvas.create_text(a+b,a,text="Save",font="Harrington 18")
    canvas.create_text(a+c,a,text="Load",font="Harrington 18")
    canvas.create_text(a+b+c,a,text="Clear",font="Harrington 18")
    canvas.create_text(a+2*c,a,text="Power",font="Harrington 18")
    canvas.create_text(a+2*c+b,a-d,text="Tianyuan Du",font="Harrington 12 bold")
    canvas.create_text(a+2*c+b,a+d,text="tianyuad",font="Harrington 12")

#draw left button (Or)
def drawButtonOr(canvas,data):
    r,l=data.r,data.threadResidue
    a,b,c,d=50,100,200,data.unit
    canvas.create_rectangle(b+l,b+l,2*c+2*b,2*c+2*b,fill="wheat",outline="blue")
    canvas.create_line(b,b,b,2*b+2*c)
    canvas.create_line(0,b,b,b)
    canvas.create_oval(a-r,a+b-r,a+r,a+b+r,fill="black",outline="red")
    canvas.create_line(a+r,a+b,a+r+l,a+b,fill="red",width=2)
    canvas.create_text(a,a+b+2*d,text="input", font="Time 12 bold")
    canvas.create_line(0,c,b,c)
    canvas.create_oval(a-r,a+c-r,a+r,a+c+r,fill="black", outline="green")
    canvas.create_line(a-r-l,a+c,a-r,a+c,fill="green",width=2)
    canvas.create_text(a,a+c+2*d,text="output", font="Time 12 bold")
    canvas.create_line(0,b+c,b,b+c)
    canvas.create_line(a-l-d,a+b+c,a+d+2*r,a+b+c)
    canvas.create_polygon(a-d,a+b+c-d/2,a-d,a+b+c+d/2,a+d,a+b+c,fill="white",
        outline="black")
    canvas.create_oval(a+d,a+b+c-2,a+d+4,a+b+c+2,fill="white", outline="black")
    canvas.create_text(a,a+b+c+2*d,text="not", font="Time 12 bold")
    canvas.create_line(0,2*c,b,2*c)

#draw left button (Not)
def drawButtonNot(canvas,data):
    r,l=data.r,data.threadResidue
    a,b,c,d=50,100,200,data.unit
    canvas.create_rectangle(a-d,a+2*c-d,a+d,a+2*c+d, fill="white")
    canvas.create_oval(a,a+2*c-d,a+2*d,a+2*c+d,fill="white")
    canvas.create_rectangle(a-d+1,a+2*c-d+1,a+d-1,a+2*c+d-1, fill="white",
        outline="white")
    canvas.create_line(a-d-l,a+2*c-d+r,a-d,a+2*c-d+r,fill="green")
    canvas.create_line(a-d-l,a+2*c+d-r,a-d,a+2*c+d-r,fill="green")
    canvas.create_line(a+2*d,a+2*c,a+2*d+l,a+2*c,fill="red")
    canvas.create_text(a,a+2*c+2*d,text="and", font="Time 12 bold")
    canvas.create_line(0,2*c+b,b,2*c+b)
    canvas.create_polygon(a-d-r,a+b+2*c-d,a-d-r+l/2,a+b+2*c-d+l,a-d-r+l/2,
        a+b+2*c+d-l,a-d-r,a+b+2*c+d,a,a+b+2*c+d,a+d+r,a+b+2*c,a,a+b+2*c-d,
        fill="white",outline="black")
    canvas.create_line(a-d-r-l/2,a+b+2*c-d+l,a-d-r+l/2,a+b+2*c-d+l,fill="green")
    canvas.create_line(a-d-r-l/2,a+b+2*c+d-l,a-d-r+l/2,a+b+2*c+d-l,fill="green")
    canvas.create_line(a+d+r,a+b+2*c,a+d+r+l,a+b+2*c, fill="red")
    canvas.create_text(a,a+b+2*c+2*d,text="or", font="Time 12 bold")

#draw phenomenon when buttons are pressed
def drawButtonPressed(canvas,data):
    r,l=data.r,data.threadResidue
    a,b,c,d=50,100,200,data.unit
    if data.button=="input":canvas.create_rectangle(d/2,b+d/2,b-d/2,c-d/2,
                                    fill="white",outline="gray",width=d)
    elif data.button=="output": canvas.create_rectangle(d/2,c+d/2,b-d/2,b+c-d/2,
                                    fill="white",outline="gray",width=d)
    elif data.button=="not": canvas.create_rectangle(d/2,b+c+d/2,b-d/2,2*c-d/2,
                                    fill="white",outline="gray",width=d)
    elif data.button=="and": canvas.create_rectangle(d/2,2*c+d/2,b-d/2,2*c+b-d/2
                                ,fill="white",outline="gray",width=d)
    elif data.button=="or": canvas.create_rectangle(d/2,2*c+b+d/2,b-d/2,
                                2*c+2*b-d/2,fill="white",outline="gray",width=d)
    
#draw if press Save
def drawSave(canvas,data):
    a,b,c,d=50,100,200,data.unit
    if data.save==True:
        canvas.create_rectangle(b+d/2,d/2,c-d/2,b-d/2,fill="white",
            outline="gray",width=d)
        
#helper function of save pressed
def drawSaveAdd(canvas,data):
    if data.save==True:
        a,b,c=50,100,200
        canvas.create_text(a+b+c,a+b+c,text="Saved!!", font="Time 40 bold")

#location of buttons
def buttonPoint(data,x,y):
    #set r,l,d to calculate their position in a small area
    r,l,d=data.r,data.threadResidue,data.unit
    #append four elements in the list
    if data.button=="input":
        input1=Input()
        data.outpointList.append([x+r+l,y,input1,"input"])
        data.inputButtons.append([x,y,input1,"input"])
    elif data.button=="output": 
        data.inpointList.append([x-r-l,y,Output(),"output"])
    elif data.button=="and":
        and1=And()
        data.inpointList.append([x-d-l,y-d+r,and1,"and"])
        data.inpointList.append([x-d-l,y+d-r,and1,"and"])
        data.outpointList.append([x+2*d+l,y,and1,"and"])
    else: buttonPointAdd(data,x,y)
#other buttons stored
def buttonPointAdd(data,x,y):
    r,l,d=data.r,data.threadResidue,data.unit
    if data.button=="or":
        or1=Or()
        data.inpointList.append([x-d-r-l/2,y-d+l,or1,"or"])
        data.inpointList.append([x-d-r-l/2,y+d-l,or1,"or"])
        data.outpointList.append([x+d+r+l,y,or1,"or"])
    elif data.button=="not":
        not1=Not()
        data.inpointList.append([x-l-d,y,not1,"not"])
        data.outpointList.append([x+d+2*r,y,not1,"not"])
#helper function gets distance
def distance(a,b):
    return ((a[0]-b[0])**2+(a[1]-b[1])**2)**(0.5)

#mouse pressed to select gates
def mousePressedLeftButton(event,data):
    a,b,c,d=50,100,200,data.unit
    if event.y >b and event.y<c:
        data.button = "input"
    elif event.y> c and event.y< b+c:
        data.button = "output"
    elif event.y>b+c and event.y < 2*c:
        data.button = "not"
    elif event.y>2*c and event.y<2*c+b:
        data.button="and"
    elif event.y>2*c+b and event.y<2*c+2*b:
        data.button="or"

#mouse pressed to set gates
def mousePressedSetGates(event,data):
    if data.button in data.buttonDict:
        data.buttonDict[data.button].append((event.x, event.y))
    else:
        data.buttonDict[data.button]=[(event.x,event.y)]
    buttonPoint(data,event.x,event.y)
    data.button=None

#line connection
def connectLine(event,data):
    a,b,c,d=50,100,200,data.unit
    minDistance=b*data.unit
    if data.connectLine==[]:          
        for point in data.outpointList:
            if distance([(point[0]),(point[1])],[event.x,event.y])<minDistance:
                minDistance=distance([(point[0]),(point[1])],[event.x,event.y])
                minPoint=point
        if minDistance<data.errorBound: data.connectLine.append(minPoint)
    else:
        for point in data.inpointList:
            if distance(point,[event.x,event.y])<minDistance:
                minDistance=distance(point,[event.x,event.y])
                minPoint=point
        if minDistance<data.errorBound:
            data.connectLine.append(minPoint)
            data.inpointList.remove(minPoint)
            data.lineList.append(data.connectLine)
            data.connectLine[0][2].connectTo(data.connectLine[1][2])
            data.connectLine=[]
            
#switch the power state as user click power.
def powerSwitch(event,data):
    if data.power==False:#not gate works
        for index in range(len(data.inputButtons)):
            data.inputButtons[index][2].setInputValue(None,False)
    else:
        for index in range(len(data.inpointList)):
            data.inpointList[index][2].inputVals=None
            data.inpointList[index][2].outputValue=None
        for index in range(len(data.outpointList)):
            data.outpointList[index][2].inputVals=None
            data.outpointList[index][2].outputValue=None
    data.power= not data.power #switch the power state

#control when power is get
def powerGet(event,data):
    b=100
    minDistance=b*data.unit
    for index in range(len(data.inputButtons)): 
        xi,yi=int(data.inputButtons[index][0]),int(data.inputButtons[index][1])
        if distance([xi,yi],[event.x,event.y])<minDistance:
            minDistance=distance([xi,yi],[event.x,event.y])
            minPoint=data.inputButtons[index]
    if minDistance<data.errorBound:
        minPoint[2].setInputValue(None,not minPoint[2].outputValue)
#control when mouse is pressed
def mousePressed(event, data):
    a,b,c,d=50,100,200,data.unit
    if event.x < b and data.power==False: mousePressedLeftButton(event,data)  
    elif event.x>b and event.x<2*c+2*b-a/2 and event.y>b and data.power==False:
        if data.button!=None: mousePressedSetGates(event,data)
        else:connectLine(event,data)
    elif event.x>b+c and event.x<2*c and event.y<b: 
        clear(data)
    elif event.x>2*c and event.x<2*c+b and event.y<b: 
        powerSwitch(event,data)
    else:
        if data.power==True:
            #when power is on
            if event.x>b and event.x<2*c+2*b-a/2 and event.y>b:
                powerGet(event,data)
        elif event.x>c and event.x<b+c and event.y<b: 
            init(data)
            load(data)
        elif event.x>b and event.x<c and event.y<b: 
            printFile(data,data.path,data.contents)
            printFile(data,data.path,data.contents)
#clear out the data
def clear(data):
    init(data)

#load the files
def readFile(data):
    with open(data.path, "rt") as f:
        data.read=f.read()
        return
#load data
def load(data):
    readFile(data)
    loadinput(data)
    loadInpoint(data)
    loadOutpointList(data)
    loadlineList(data)
    loaddict(data)
#helper function gets the gate
def getGate(name):
    gate = None
    if(name == "input"):
        gate = Input()
    elif(name == "output"):
        gate = Output()
    elif(name == "and"):
        gate = And()
    elif(name == "or"):
        gate = Or()
    elif(name == "not"):
        gate = Not()#create a new object in the list data.gate
    return gate
#load input
def loadinput(data):
    length=len("#below are inputButtons\n")
    startPoint=data.read.find("#below are inputButtons\n")+length
    endPoint=data.read.find("#below are inpointList")
    inputStr=data.read[startPoint:endPoint]
    for lines in inputStr.splitlines():
        inputs=lines.split(",")
        inputs[0],inputs[1]=int(inputs[0]),int(inputs[1])
        if inputs[2] not in data.location:
            data.location.append(inputs[2])
            k=(inputs[-1][1:])#inputs[-1][1:] is actually the "input"
            gate = getGate(k)
            data.gate.append(gate)
        index=data.location.index(inputs[2])
        inputs[2]=data.gate[index]
        data.inputButtons.append(inputs)#recover the inputButton list
#below are similar to the first function
def loadInpoint(data):
    length=len("#below are inpointList\n")
    startPoint=data.read.find("#below are inpointList\n")+length
    endPoint=data.read.find("#below are outpointList")
    inpointStr=data.read[startPoint:endPoint]
    for lines in inpointStr.splitlines():
        inpoint=lines.split(",")
        inpoint[0],inpoint[1]=int(inpoint[0]),int(inpoint[1])
        if inpoint[2] not in data.location:
            data.location.append(inpoint[2])
            k=(inpoint[-1][1:])
            gate = getGate(k)
            data.gate.append(gate)
        index=data.location.index(inpoint[2])
        inpoint[2]=data.gate[index]
        data.inpointList.append(inpoint)
#load the list of outpointers
def loadOutpointList(data):
    length=len("#below are outpointList\n")
    startPoint=data.read.find("#below are outpointList\n")+length
    endPoint=data.read.find("#below are lines")
    outpointStr=data.read[startPoint:endPoint]
    for lines in outpointStr.splitlines():
        outpoint=lines.split(",")
        outpoint[0],outpoint[1]=int(outpoint[0]),int(outpoint[1])
        if outpoint[2] not in data.location:
            data.location.append(outpoint[2])
            k=(outpoint[-1][1:])
            gate=getGate(k)
            data.gate.append(gate)
        index=data.location.index(outpoint[2])
        outpoint[2]=data.gate[index]
        data.outpointList.append(outpoint)
#load the list of lines
def loadlineList(data):
    length=len("#below are lines\n")
    startPoint=data.read.find("#below are lines\n")+length
    endPoint=data.read.find("#below are dicts")
    lineStr=data.read[startPoint:endPoint]
    for lines in lineStr.splitlines():
        line=lines.split(",")
        line[0],line[1]=int(float(line[0])),int(float(line[1]))
        if line[2] not in data.location:
            data.location.append(line[2])
            k=(line[-1][1:])
            gate = getGate(k)
            data.gate.append(gate)
        index=data.location.index(line[2])
        line[2]=data.gate[index]
        data.connectLine.append(line)
        print(data.connectLine)
        if len(data.connectLine)==2:
            data.connectLine[0][2].connectTo(data.connectLine[1][2])
            data.lineList.append(data.connectLine)
            data.connectLine=[]
#load dictionaries of all states
def loaddict(data):
    length=len("#below are dicts\n")
    startPoint=data.read.find("#below are dicts\n")+length
    dictStr=data.read[startPoint:]
    dictInput(data,dictStr)
    dictOutput(data,dictStr)
    dictAnd(data,dictStr)
    dictOr(data,dictStr)
    dictNot(data,dictStr)
#find the endpoint of system
def findEndPoint(string,start):
    for index in range(start,len(string)):
        if string[index] in "ioan":
            return index
    return -1

#set input of dictionary
def dictInput(data,dictstr):    
    inputlen=len("input\n")
    if data.read.find("input\n")!=-1:
        start=dictstr.find("input\n")+inputlen
        end=findEndPoint(dictstr,start)
        for line in dictstr[start:end].splitlines():
            if "input" in data.buttonDict:
                data.buttonDict["input"].append(line.split(","))
            else:
                data.buttonDict["input"]=[line.split(",")]
#set output of dictionary
def dictOutput(data,dictstr):
    outputlen=len("output\n")
    if data.read.find("output\n")!=-1:
        start=dictstr.find("output\n")+outputlen
        end=findEndPoint(dictstr,start)
        for line in dictstr[start:end].splitlines():
            if "output" in data.buttonDict:
                data.buttonDict["output"].append(line.split(","))
            else:
                data.buttonDict["output"]=[line.split(",")]
#and dictionary
def dictAnd(data,dictstr):
    andlen=len("and\n")
    if data.read.find("and\n")!=-1:
        start=dictstr.find("and\n")+andlen
        end=findEndPoint(dictstr,start)
        for line in dictstr[start:end].splitlines():
            if "and" in data.buttonDict:
                data.buttonDict["and"].append(line.split(","))
            else:
                data.buttonDict["and"]=[line.split(",")]
#or dictionary
def dictOr(data,dictstr):
    orlen=len("or\n")
    if data.read.find("or\n")!=-1:
        start=dictstr.find("or\n")+orlen
        end=findEndPoint(dictstr,start)
        for line in dictstr[start:end].splitlines():
            if "or" in data.buttonDict:
                data.buttonDict["or"].append(line.split(","))
            else:
                data.buttonDict["or"]=[line.split(",")]
#not dictionary
def dictNot(data,dictstr):
    notlen=len("not\n")
    if data.read.find("not\n")!=-1:
        start=dictstr.find("not\n")+notlen
        end=findEndPoint(dictstr,start)
        for line in dictstr[start:end].splitlines():
            if "not" in data.buttonDict:
                data.buttonDict["not"].append(line.split(","))
            else:
                data.buttonDict["not"]=[line.split(",")]


#save file
def printFile(data,path,contents):
    save(data)
    with open(path, "wt") as f:
        f.write(contents)
#save data
def save(data):
    data.save=True
    data.contents=""
    saveInputButtons(data)
    saveInpointList(data)
    saveOutpointList(data)
    saveLines(data)
    saveContents(data)
#save input buttons
def saveInputButtons(data):
    data.contents+="#below are inputButtons\n"
    for index in range(len(data.inputButtons)):
        position=str(data.inputButtons[index]).find("'")
        data.contents+=str(data.inputButtons[index])[1:position]
        data.contents+=str(data.inputButtons[index])[position+1:-2]+"\n"
#save inpoint lists
def saveInpointList(data):
    data.contents+="#below are inpointList\n"
    for index in range(len(data.inpointList)):
        position=str(data.inpointList[index]).find("'")
        data.contents+=str(data.inpointList[index])[1:position]
        data.contents+=str(data.inpointList[index])[position+1:-2]+"\n"
#save outpoint lists
def saveOutpointList(data):
    data.contents+="#below are outpointList\n"
    for index in range(len(data.outpointList)):
        position=str(data.outpointList[index]).find("'")
        data.contents+=str(data.outpointList[index])[1:position]
        data.contents+=str(data.outpointList[index])[position+1:-2]+"\n"
#save contents
def saveContents(data):
    data.contents+="#below are dicts\n"
    for key in data.buttonDict:
        data.contents+=key
        data.contents+="\n"
        for index in range(len(data.buttonDict[key])):
            data.contents+=str(data.buttonDict[key][index])[1:-1]+"\n"
#save lines of data
def saveLines(data):
    data.contents+="#below are lines\n"
    for index in range(len(data.lineList)):
        position=str(data.lineList[index][0]).find("'")
        data.contents+=str(data.lineList[index][0])[1:position]
        data.contents+=str(data.lineList[index][0])[position+1:-2]+"\n"
        position=str(data.lineList[index][1]).find("'")
        data.contents+=str(data.lineList[index][1])[1:position]
        data.contents+=str(data.lineList[index][1])[position+1:-2]+"\n"

#when key is pressed
def keyPressed(event, data):
    pass
#when time passes
def timerFired(data):
    data.save=False
#draw the animation
def redrawAll(canvas, data):
    drawButtonPressed(canvas,data)
    drawButtonAnd(canvas,data)
    drawButtonOr(canvas,data)
    drawButtonNot(canvas,data)
    drawGate(canvas,data)
    drawGateAdd(canvas,data)
    drawPowerLine(canvas,data)
    drawPowerInput(canvas,data)
    drawSaveAdd(canvas,data)

def run(width=600, height=600):
    #run redrawAll
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    
    #run mousepressed
    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)
    #run keypressed
    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)
    #run timerfired
    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 1000 # milliseconds
    init(data)
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    root.mainloop()  # blocks until window is closed
    print("bye!")

run()
print(findRTP(8))
