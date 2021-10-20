#from IPython import get_ipython;
#get_ipython().magic('reset -sf')

# import Tkinter
import tkinter as tk

# import SerialComms
import SerialComms

# import serial exception handler
from serial import SerialException

comPort = 'COM3'
baudRate = 9600


# create a widow
window = tk.Tk()

# give the window a title
window.title("Design (E.) 344")

# define the dimensions of the window
windowWidth = 1024;  # width in pixels
windowHeight = 720;  # height in pixels

# make the window pop up in the middle of the display, on any size display
widthSystem = window.winfo_screenwidth()  # get width of current screen
heightSystem = window.winfo_screenheight()  # get height of current screen
windowX = (widthSystem / 2) - (windowWidth / 2)  # set the horizontal location of the window
windowY = (heightSystem / 2) - (windowHeight / 2)  # set the vertical location of the window
window.geometry('%dx%d+%d+%d' % (windowWidth, windowHeight, windowX, windowY))  # set the location of the window
window.resizable(True, True)

# creates an instance of the SerialComms class
sc = SerialComms.SerialComms(comPort, baudRate)

# creates label
connectionLabelText = "Enter your Baud rate and COM Port below, and click connect."
connectionLabel = tk.Label(text=connectionLabelText)
connectionLabel.grid(column=0, row=0, columnspan=2)

# creates label
baudLabelText = "Baud Rate"
baudLabel = tk.Label(text=baudLabelText)
baudLabel.grid(column=0, row=1)

# creates label
comLabelText = "COM Port:"
comLabel = tk.Label(text=comLabelText)
comLabel.grid(column=0, row=2)

# creates an entry box for the user to enter the baud rate
entryBaudRate = tk.Entry()
entryBaudRate.grid(column=1, row=1)
entryBaudRate.insert(0, baudRate)

# creates an entry box for the user to enter the COM port
entryComPort = tk.Entry(text=comPort)
entryComPort.grid(column=1, row=2)
entryComPort.insert(0, comPort)

# creates a label indicating the current connection status
connectionStatusLabelText = "The device is currently disconnected."
connectionStatusLabel = tk.Label(text=connectionStatusLabelText)
connectionStatusLabel.grid(column=0, row=4, columnspan=2)

# creates a connect/disconnect button
connectionButtonText = "Toggle Connection"
connectionButton = tk.Button(text=connectionButtonText, command=lambda: buttonConnectHandler())
connectionButton.grid(column=0, row=3, columnspan=2)


#Create a Start Charging Button
StartChargingButtonText = "Start Charging Battery"
StartChargingButton = tk.Button(text=StartChargingButtonText, command=lambda: buttonStartChargingHandler())
StartChargingButton.grid(column=0, row=7, columnspan=2)

# creates a label indicating the current charging status
chargingStatusLabelText = "The Battery is currently charging."
chargingStatusLabel = tk.Label(text=chargingStatusLabelText)
chargingStatusLabel.grid(column=0, row=8, columnspan=2)

#Create a Stop Charging Button
StopChargingButtonText = "Stop Charging Battery"
StopChargingButton = tk.Button(text=StopChargingButtonText, command=lambda: buttonStopChargingHandler())
StopChargingButton.grid(column=0, row=9, columnspan=2)

#Define battery voltage label
batteryVoltage = tk.StringVar()
# creates label showing the Battery Voltage Text
batteryVoltageLabelStatic = tk.Label(text="Battery Voltage [V]: ")
batteryVoltageLabelStatic.grid(column=0, row=15, columnspan=2)
#creates label showing the Battery Voltage Changing
batteryVoltageLabelVariable = tk.Label(textvariable=batteryVoltage)
batteryVoltageLabelVariable.grid(column=1, row=15, columnspan=1)

#Define supply voltage label
supplyVoltage = tk.StringVar()
# creates label showing the supply Voltage Text
supplyVoltageLabelStatic = tk.Label(text="Supply Voltage [V]: ")
supplyVoltageLabelStatic.grid(column=0, row=16, columnspan=2)
#creates label showing the supply Voltage Changing
supplyVoltageLabelVariable = tk.Label(textvariable=supplyVoltage)
supplyVoltageLabelVariable.grid(column=1, row=16, columnspan=1)

#Define battery current label
batteryCurrent = tk.StringVar()
# creates label showing the Battery Current Text
batteryCurrentLabelStatic = tk.Label(text="Battery Current [A]: ")
batteryCurrentLabelStatic.grid(column=0, row=17, columnspan=2)
#creates label showing the Battery Current Changing
batteryCurrentLabelVariable = tk.Label(textvariable=batteryCurrent)
batteryCurrentLabelVariable.grid(column=1, row=17, columnspan=1)

#Define ambient light level label
ambientLightLevel = tk.StringVar()
# creates label showing the Battery Current Text
ambientLightLevelLabelStatic = tk.Label(text="Ambient LightLevel [%]: ")
ambientLightLevelLabelStatic.grid(column=0, row=18, columnspan=2)
#creates label showing the Battery Current Changing
ambientLightLevelLabelVariable = tk.Label(textvariable=ambientLightLevel)
ambientLightLevelLabelVariable.grid(column=1, row=18, columnspan=1)

# updates the display every 100 ms
def updateDisplay():
    # update the variables that you want to stay current here
    if (sc.isOpen == True):
        data = sc.receive()
        if (len(data) == 1):
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


        data = ""

    window.after(100, lambda: updateDisplay())


def openConnection(sc):
    sc.setCOMPort(comPort)
    sc.setBaudrate(baudRate)
    sc.open()


def closeConnection(sc):
    sc.close()


def buttonConnectHandler():
    global comPort
    global baudRate

    # If the connection is closed, try open it.
    if (sc.isOpen == False):
        comPort = entryComPort.get()
        baudRate = entryBaudRate.get()

        # Tries to open the serial conection. Displays error message in ConnectFeedback if it fails.
        try:
            openConnection(sc);
        except SerialException:
            print("Unable to connect.")

        if (sc.isOpen == True):
            print("Connected successfully.")
            connectionStatusLabel.configure(text="The device is currently connected.")

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


def buttonStartChargingHandler():
    if (sc.isOpen == True):
        sc.send("OV1")
        #chargingStatusLabel.configure(text="The Battery is currently charging.")

def buttonStopChargingHandler():
    if (sc.isOpen == True):
        sc.send("OV0")
        #chargingStatusLabel.configure(text="The Battery is not currently charging.")

updateDisplay()

window.mainloop()