# import Tkinter
import tkinter as tk
from tkinter import ttk

# import SerialComms
import SerialComms

# import serial exception handler
from serial import SerialException
from PIL import Image, ImageTk

comPort = 'COM5'
baudRate = 9600
connectionBoolStatus=0
startUpCounter = 0
mode = "manual"



# create a widow
def mainWin():
    print("I have been called")
    splashWindow.destroy()
    window = tk.Tk()
    #create canvas
    canvas=tk.Canvas(window,width=800,height=600)
    canvas.grid(rowspan=51,columnspan=5)

    # give the window a title
    window.title("Design (E.) 344 23252162")

    # define the dimensions of the window
    windowWidth = 800  # width in pixels
    windowHeight = 600  # height in pixels

    # make the window pop up in the middle of the display, on any size display
    widthSystem = window.winfo_screenwidth()  # get width of current screen
    heightSystem = window.winfo_screenheight()  # get height of current screen
    windowX = (widthSystem / 2) - (windowWidth / 2)  # set the horizontal location of the window
    windowY = (heightSystem / 2) - (windowHeight / 2)  # set the vertical location of the window
    window.geometry('%dx%d+%d+%d' % (windowWidth, windowHeight, windowX, windowY))  # set the location of the window
    window.resizable(True, True)

    # creates label
    connectionLabelText = "Enter your Baud rate and COM Port below, and click connect."
    connectionLabel = tk.Label(text=connectionLabelText)
    connectionLabel.grid(column=2, row=0)

    # creates label
    baudLabelText = "Baud Rate:"
    baudLabel = tk.Label(text=baudLabelText)
    baudLabel.grid(column=2, row=1,sticky='w',padx = (30, 0))
    #

    # creates label
    comLabelText = "COM Port:"
    comLabel = tk.Label(text=comLabelText)
    comLabel.grid(column=2, row=2,sticky='w',padx = (30, 0),pady = (0, 20))

    # creates an entry box for the user to enter the baud rate
    entryBaudRate = tk.Entry()
    entryBaudRate.grid(column=2, row=1  ,padx = (0, 60))
    entryBaudRate.insert(0, baudRate)

    # creates an entry box for the user to enter the COM port
    entryComPort = tk.Entry(text=comPort)
    entryComPort.grid(column=2, row=2,padx = (0, 60),pady = (0, 20))
    entryComPort.insert(0, comPort)

    # creates a label indicating the current connection status
    connectionStatusLabelText = "The device is currently disconnected."
    connectionStatusLabel = tk.Label(text=connectionStatusLabelText)
    connectionStatusLabel.grid(column=2, row=3)

    # creates a connect/disconnect button
    connectionButtonText = "Toggle Connection"
    connectionButton = tk.Button(text=connectionButtonText, command=lambda: buttonConnectHandler())
    connectionButton.grid(column=2, row=3,pady = (0, 50))

    # Create a Start Charging Button
    StartChargingButtonText = "Start Charging Battery"
    StartChargingButton = tk.Button(text=StartChargingButtonText, bg='black', fg='white', command=lambda: buttonStartChargingHandler())
    StartChargingButton.grid(column=0, row=4, columnspan=2)

    # creates a label indicating the current charging status
    chargingStatusLabelText = "The Battery is not currently charging."
    chargingStatusLabel = tk.Label(text=chargingStatusLabelText)
    chargingStatusLabel.grid(column=0, row=5, columnspan=2)

    # Create a Stop Charging Button
    StopChargingButtonText = "Stop Charging Battery"
    StopChargingButton = tk.Button(text=StopChargingButtonText, bg='black', fg='white',command=lambda: buttonStopChargingHandler())
    StopChargingButton.grid(column=0, row=6, columnspan=2)


    # Define battery voltage label
    batteryVoltage = tk.StringVar()
    # creates label showing the Battery Voltage Text
    batteryVoltageLabelStatic = tk.Label(text="Battery Voltage [V]: ")
    batteryVoltageLabelStatic.grid(padx=(0,50),column=1, row=10, columnspan=2)
    batteryVoltageLabelStatic.config(padx=25,pady=15,bg='lightblue')
    # creates label showing the supply Voltage Changing
    batteryVoltageLabelVariable = tk.Label(textvariable=batteryVoltage)
    batteryVoltageLabelVariable.grid(column=1, row=10,padx = (100, 0), columnspan=2)
    batteryVoltageLabelVariable.config(pady=15, bg='lightblue')


    # Define supply voltage label
    supplyVoltage = tk.StringVar()
    # creates label showing the supply Voltage Text
    supplyVoltageLabelStatic = tk.Label(text="Supply Voltage [V]: ")
    supplyVoltageLabelStatic.grid(column=2, row=10, columnspan=2,padx=(170,0))
    supplyVoltageLabelStatic.config(padx=25, pady=15, bg='lightblue')
    # creates label showing the supply Voltage Changing
    supplyVoltageLabelVariable = tk.Label(textvariable=supplyVoltage)
    supplyVoltageLabelVariable.grid(column=2, row=10, columnspan=2,padx = (300, 0))
    supplyVoltageLabelVariable.config(pady=15, bg='lightblue')


    # Define battery current label
    batteryCurrent = tk.StringVar()
    # creates label showing the Battery Current Text
    batteryCurrentLabelStatic = tk.Label(text="Battery Current [A]: ")
    batteryCurrentLabelStatic.grid(padx=(0,50),column=1, row=11, columnspan=2)
    batteryCurrentLabelStatic.config(padx=25, pady=15, bg='lightblue')
    # creates label showing the Battery Current Changing
    batteryCurrentLabelVariable = tk.Label(textvariable=batteryCurrent)
    batteryCurrentLabelVariable.grid(column=1, row=11,padx = (90, 0), columnspan=2)
    batteryCurrentLabelVariable.config(pady=15,bg='lightblue')


    # Define ambient light level label
    ambientLightLevel = tk.StringVar()
    # creates label showing the Battery Current Text
    ambientLightLevelLabelStatic = tk.Label(text="Ambient LightLevel [%]: ")
    ambientLightLevelLabelStatic.grid(column=2, row=11, columnspan=2,padx=(170,0))
    ambientLightLevelLabelStatic.config(padx=10, pady=15, bg='lightblue')
    # creates label showing the Battery Current Changing
    ambientLightLevelLabelVariable = tk.Label(textvariable=ambientLightLevel)
    ambientLightLevelLabelVariable.grid(column=2, row=11, columnspan=2,padx = (320, 0))
    ambientLightLevelLabelVariable.config(pady=15, bg='lightblue')

    #Create PWM Slider
    sliderPWM= tk.Scale(window, from_=0, to=100, orient='horizontal')
    sliderPWM.grid(column=2, row=15)
    sliderPWM.set(100)

    def getsliderPWMValue():
        pwmValue=sliderPWM.get()
        pwmValue=str(pwmValue)
        if (sc.isOpen == True):
            sc.send(pwmValue)

    pwmValueButton = tk.Button(text="Send Manual PWM Value", command=lambda: getsliderPWMValue())
    pwmValueButton .grid(column=2, row=16,padx=5,pady=5)

    pwmManualButton = tk.Button(text="Manual PWM Mode", command=lambda: pwmManualButtonHandler())
    pwmManualButton.grid(column=2, row=16, padx=(0,350), pady=5)

    pwmAutomaticButton = tk.Button(text="Automatic PWM Mode", command=lambda: pwmAutomaticButtonHandler())
    pwmAutomaticButton.grid(column=2, row=16, padx=(360,0), pady=5)

    # Define ambient light level label
    pwmLevel = tk.StringVar()
    # creates label showing the Battery Current Text
    pwmLevelLabelStatic = tk.Label(text="Current PWM Value [%]: ")
    pwmLevelLabelStatic.grid(column=2, row=17, columnspan=1)
    pwmLevelLabelStatic.config(padx=25, pady=15, bg='lightblue')
    # creates label showing the Battery Current Changing
    pwmLevelLabelVariable = tk.Label(textvariable=pwmLevel)
    pwmLevelLabelVariable.grid(column=2, row=17, columnspan=1, padx=(175, 0))
    pwmLevelLabelVariable.config(pady=15, bg='lightblue')


    def buttonConnectHandler():
        global comPort
        global baudRate
        global connectionBoolStatus

        # If the connection is closed, try open it.
        if (sc.isOpen == False):
            comPort = entryComPort.get()
            baudRate = entryBaudRate.get()

            # Tries to open the serial conection. Displays error message in ConnectFeedback if it fails.
            try:
                openConnection(sc)
            except SerialException:
                print("Unable to connect.")

            if (sc.isOpen == True):
                print("Connected successfully.")
                connectionStatusLabel.configure(text="The device is currently connected.")
                connectionBoolStatus = 1
                print(connectionBoolStatus)

        # If the connection is open, close it.
        elif (sc.isOpen == 1):
            # Tries to close the serial conection. Displays error message in ConnectFeedback if it fails.
            try:
                closeConnection(sc)
            except SerialException:
                print("Unable to close connection.")
            # If the connection is closed, change the label of the button and and update ConnectFeedback to disconnected.
            if (sc.isOpen == False):
                print("Disconnected successfully.")
                connectionStatusLabel.configure(text="The device is currently disconnected.")
                connectionBoolStatus = 0
                print(connectionBoolStatus)

    def buttonStartChargingHandler():
        StopChargingButton.config(bg="black", fg="white")
        StartChargingButton.config(bg="green", fg="white")
        if (sc.isOpen == True):
            sc.send("OV1")

    def buttonStopChargingHandler():
        StartChargingButton.config(bg="black", fg="white")
        StopChargingButton.config(bg="red", fg="white")
        if (sc.isOpen == True):
            sc.send("OV0")

    def pwmManualButtonHandler():
        pwmAutomaticButton.config(bg="black", fg="white")
        pwmManualButton.config(bg="blue", fg="white")
        if (sc.isOpen == True):
            global mode
            mode = "manual"
            sc.send("manual")

    def pwmAutomaticButtonHandler():
        pwmManualButton.config(bg="black", fg="white")
        pwmAutomaticButton.config(bg="blue", fg="white")
        if (sc.isOpen == True):
            global mode
            mode = "automatic"
            sc.send("automatic")


    # updates the display every 100 ms
    def updateDisplay():
        # update the variables that you want to stay current here
        #pwmValue = sliderPWM.get()
        #print(pwmValue)
        if (sc.isOpen == True):
            data = sc.receive()
            if ((len(data) == 1) & (data!=[] and data[0].count(',')==6)):
                print(data[0])
                inputData = data[0].split(',')
                if (inputData[0] == '1'):
                    print("The Battery is currently charging.")
                    chargingStatusLabel.configure(text="The Battery is currently charging.")
                elif (inputData[0] == '0'):
                    print("The Battery is not currently charging.")
                    chargingStatusLabel.configure(text="The Battery is not currently charging.")
                batteryVoltage.set(inputData[1])
                supplyVoltage.set(inputData[2])
                batteryCurrent.set(inputData[3])
                ambientLightLevel.set(inputData[4])
                if(mode == "manual"):
                    print("manual")
                    pwmLevelInt=int(int(inputData[5])/2.52)
                    pwmLevel.set(pwmLevelInt)
                elif(mode == "automatic"):
                    print("automatic")
                    pwmLevelInt = int(int(inputData[6]) / 2.52)
                    pwmLevel.set(pwmLevelInt)


            data = ""

        window.after(100, lambda: updateDisplay())

    updateDisplay()







#Create A Splash Screen
splashWindow = tk.Tk()
splashWindow.title("Design (E.) 344 23252162")

# define the dimensions of the window
splashWindowWidth = 1024  # width in pixels
splashWindowHeight = 700  # height in pixels

#Remove border of the splash Window
splashWindow.overrideredirect(False)

#Define the label of the window
splashWindowLabel = tk.Label(text= "Built by AA. Cilliers 23252162", fg= "blue")
splashWindowLabel.grid(column=0, row=2)

logo = Image.open('D:/Univsersity/2021-3rd Year S2/Design (E) - 344/GitRepo/E344/Python/Edesign344V2/logo.png')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(column=0,row=0)

# make the window pop up in the middle of the display, on any size display
widthSystem = splashWindow.winfo_screenwidth()  # get width of current screen
heightSystem = splashWindow.winfo_screenheight()  # get height of current screen
windowX = (widthSystem / 2) - (splashWindowWidth / 2)  # set the horizontal location of the window
windowY = (heightSystem / 2) - (splashWindowHeight / 2)  # set the vertical location of the window
splashWindow.geometry('%dx%d+%d+%d' % (splashWindowWidth, splashWindowHeight, windowX, windowY))  # set the location of the window
splashWindow.resizable(False, False)

# creates an instance of the SerialComms class
sc = SerialComms.SerialComms(comPort, baudRate)



def openConnection(sc):
    sc.setCOMPort(comPort)
    sc.setBaudrate(baudRate)
    sc.open()


def closeConnection(sc):
    sc.close()





print(connectionBoolStatus)
#updateDisplay()
splashWindow.after(3500,mainWin)
splashWindow.mainloop()


