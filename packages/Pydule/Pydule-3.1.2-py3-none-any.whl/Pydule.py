import datetime
import os
import pyttsx3 
import pywhatkit as kt
import playsound as ps
import requests
from deep_translator import GoogleTranslator
from bs4 import BeautifulSoup
from datetime import date,datetime
from playsound import playsound
from tkinter import *
from tkinter import colorchooser
from AppOpener import open

engine = pyttsx3.init() 

def module_needed():
	print('Hello!!\n\nYou Need to Install the Following Modules to Use Pydule Module\n\n1.playsound\n2.pywhatkit\n3.AppOpener\n4.pyttsx3\n5.datetime\n6.beautifulsoup4\n7.requests\n\nThanks for Using Pydule..')

def translate(content,language):
	translated = GoogleTranslator(source='auto', target=language).translate(content)
	print(translated)
	return translated

def info():
	print('\nThis Module Pydule is Created by D.Tamil Mutharasan\n')

def restr(oldstr,index,newstr):
	new=''
	for i in range(len(oldstr)):
		if i==index:
			new+=newstr
		else:
			new+=oldstr[i]
	return new

def relist(oldlist,index,newlist):
	new=[]
	for i in range(len(oldlist)):
		if i==index:
			new+=[newlist]
		else:
			new+=[oldlist[i]]
	return new

def retuple(oldtup,index,newtup):
	new=tuple()
	for i in range(len(oldtup)):
		if i==index:
			new+=(newtup,)
		else:
			new+=(oldtup[i],)
	return new

def clist(mx):
	List=[]
	print('Enter Values One by One\n')
	for i in range(mx):
		l=eval(input('Enter Value :'))
		List.append(l)
	print('\nList Created Sucessfully\n')
	return List

def ctuple(mx):
	Tuple=()
	print('Enter Values One by One\n')
	for i in range(mx):
		t=eval(input('Enter Value :'))
		Tuple+=(t,)
	print('\nTuple Created Sucessfully\n')
	return Tuple

def cdict(mx):
	Dict={}
	for i in range(mx):
		key=eval(input(f'Enter the Key of No.{i+1} Element :'))
		value=eval(input(f'Enter the Value of No.{i+1} Element :'))
		Dict[key]=value
	print('\nDictionary Created Sucessfully')	
	return Dict

def cset(mx):
	Set=set()
	print('Enter Values One by One\n')
	for i in range(mx):
		s=eval(input('Enter Values : '))
		Set.add(s)
	print('\nSet Created Sucessfully')	
	return Set

def pick_color():
	try:
		root=Tk()
		root.geometry('250x100')
		root.title('Color Picker')
		def n():
			c=colorchooser.askcolor(title='CP')
			print(c)
		b=Button(root,text='Pick Color',command=n).pack()
		root.mainloop()				
	except:
		print('\nSomething Went Wrong!!\n')

def open_app(app_name):
	try:
		open(app_name)
	except:
		print('\nSomething Went Wrong!!\n')	

def search(content):
	try:
		kt.search(content)	
		print('\nSearching...\n')		
	except:
		print('\nSomething Went Wrong!!\n')	

def play_song(song_path):
	try:
		playsound(song_path)
	except:
		print('\nSomething Went Wrong!!\n')	

def restart_system():
	try:
		print('\nRestarting the System...\n')		
		os.system("shutdown /r /t 1")
	except:
		print('\nSomething Went Wrong!!\n')	

def shutdown_system():
	try:
		print('\nShutting Down Your System....\n')
		return os.system("shutdown /s /t 1")
	except:
		print('\nSomething Went Wrong!!\n')		

def todays_date():
	try:
		d=date.today()
		print(f"\nTodays Date is {d}\n")
	except:
		print('\nSomething Went Wrong!!\n')	

def time_now():
	try:
		now = datetime.now()
		current_time = now.strftime("%H:%M:%S %p")
		print(f"\nCurrent Time : {current_time}\n")
	except:
		print('\nSomething Went Wrong!!\n')	

def say(content):	
	try:
		print('Converting text to Speech...') 
		engine.say(content)
		engine.runAndWait()  
	except:
		print('\nSomething Went Wrong!!\n')

def open_file(path):
	try:
		print('Opening...')
		os.startfile(path)
	except:
		print('\nSomething Went Wrong!!\n')		

def weather_now():
	try:
		headers = {
		    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


		def weather(city):
		    city = city.replace(" ", "+")
		    res = requests.get(
		        f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
		    print("Searching...\n")
		    soup = BeautifulSoup(res.text, 'html.parser')
		    location = soup.select('#wob_loc')[0].getText().strip()
		    time = soup.select('#wob_dts')[0].getText().strip()
		    info = soup.select('#wob_dc')[0].getText().strip()
		    weather = soup.select('#wob_tm')[0].getText().strip()
		    print(location)
		    print(info)
		    print(weather+"°C")


		city = input("Enter the Name of City : ")
		city = city+" weather"
		weather(city)
	except:	
		print('\nSomething Went Wrong!!\n')

def change_voice(num):
	if num<=2:
		try:
			voices=engine.getProperty('voices')
			engine.setProperty('voice',voices[num].id)
			print('\nVoice Changed Successfully\n')	
		except:
			print('\nSomething Went Wrong!!\n')
	else:
		print('\nVoice Not Found\n')		

def voice_rate(num):
	try:
		engine.setProperty('rate',num)
	except:
		print('Something Went Wrong!!\n')				