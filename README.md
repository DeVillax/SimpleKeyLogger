# SimpleKeyLogger
Simple KeyLogger made with Python for cybersecurity. 

It has screnshoot capabilities as well as extraction of data collected via email.

## 2) Dependencies

* Pynput 
* Pywin32
* Pillow

## 3) How it works

Keylogger class accepts two parameters
* destination: The email address you wish to send the logs to.
* time: Total time the Keylogger will be collected data. 

When time's up, data collected will be compressed and send via email to the given address. If no time is provided, the program will run
until 'Esc' key is issued.

Please bear in mind that data is only sent when the time paramenter is given, otherwise, the program will just capture keystrokes and stored them in the 'app.log' file.

1. Run it as a regular logger:
  ```
  from keylogger import Keylogger
  
  klogger = Keylogger()
  klogger.start()
  ```
2. Run it as a logger with email capabilities:
  ```
  from keylogger import Keylogger
  
  klogger = Keylogger("Youremail@mail.com", timeInSeconds)
  klogger.start()
  ```
  
* How words are logged

When a key is pressed, the program first checks whether the key is special or alphanumeric. If it is indeed alphanumeric, it will just append it to the last_word list. 

If the key is special, it will then check whether it is the 'space' or 'enter' keys:
   - space: It will join the letters contained in last_word and log it into the file.
   - enter: It will take a screenshot.

## 4) Assumptions

1) In order to send the email, the program will attempt to use the local outlook account configured on the device as most Windows 10 users will be using theirs by default due to the initial sign up/log in.

2) As every word is separated by space, it makes sense to log it in that way for readability purposes. 

3) Screenshots are taken when user press 'Enter' as the user is more likely to press 'enter' when logging in to a website, submitting a form and so on and so forth.


## 3) Python version used for development

Python 3.7

## 4) Reporting issues
If you find bugs, issues, or methods that could be implemented or improved,
please raise them [here](https://github.com/NcVillalobos/DeezPy/issues). Alternatively, you can contact me to my email address
'developmentvilla@gmail.com'

## 5) Feedback 

If this library is helpful for your projects, please don't hesitate reaching out
at 'developmentvilla@gmail.com', any feedback is highly appreciated.


