# Football Club Notifier is a program which sends notifications to user provided that on that day takes place a match of the user's favourite club. In total 3 notifications will be sent: in a moment of launching the program, one hour before the match and at the beginning of the match. Notifications apply to league games, Europa League and Champions League. 

## Configuration:  
Before launching the main program you have to configure it by the ```FCN config.exe``` program or the ```Config.py``` script. The configuration is to choose your favourite club. Only the first-league clubs from major european leagues are supported.  

It is recommended to put the ```Football Club Notifier.exe``` program into the startup folder.

## Source:
Both programs download the data from the site: https://www.bbc.com/sport/football  

## Caution:  
Some anti-virus softwares may classify both programs as malicious software, due to their possiblity to visit websites.

## Launch: 
* Launch the ```Main.py``` or ```Config.py``` script
* Executable (.exe) versions are available in the ```Release``` folder for both programs.

## Technology:  
* ```Python``` 3.8    
* ```requests``` 2.25.0  
* ```beautifulsoup4``` 4.9.3  
* ```plyer``` 2.0.0  
* ```pytz``` 2020.4  

## Screenshots:   
* After launching a computer:  
![FCN1](https://user-images.githubusercontent.com/71539614/99203611-5a25fb80-27b3-11eb-85fb-4ea75d08e53f.png)  
* 1 hour left:    
![FCN2](https://user-images.githubusercontent.com/71539614/99203618-5db98280-27b3-11eb-979e-7416357b798c.png)
* The match is about to start:  
![FCN3](https://user-images.githubusercontent.com/71539614/99203620-5eeaaf80-27b3-11eb-8561-5b3c02fbc944.png)  
