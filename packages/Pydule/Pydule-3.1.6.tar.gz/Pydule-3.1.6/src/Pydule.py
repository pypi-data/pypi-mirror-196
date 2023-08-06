import datetime
import os
import pyttsx3 
import pywhatkit as kt
import playsound as ps
import requests
import qrcode
from pytube import YouTube
from deep_translator import GoogleTranslator
from bs4 import BeautifulSoup
from datetime import date,datetime
from playsound import playsound
from tkinter import *
from tkinter import colorchooser
from AppOpener import open

engine = pyttsx3.init() 

err='\n \u26A0 Something Went Wrong \u26A0\n'

def translate(content,language):
	translated = GoogleTranslator(source='auto', target=language).translate(content)
	return translated

def ytmp4(link):
	try:
		yt = YouTube(link)
		stream = yt.streams.get_highest_resolution()
		stream.download()
		print('\n\U0001F3AC Video Saved Successfully \U00002714\n')
	except:
		print(err)
def ytmp3(link):
	try:
		yt = YouTube(link)
		video = yt.streams.filter(only_audio=True).first()
		ofile = video.download(output_path=".")
		b, ext = os.path.splitext(ofile)
		file = b + '.mp3'
		os.rename(ofile, file)
		print('\n\U0001F3B6 Audio Saved Successfully \U00002714\n')
	except:
		print(err)

def cqrcode(data,filename):
	try:
		img = qrcode.make(data)
		img.save(filename)
		print('\nQrcode Saved Successfully \U00002714\n')
	except:
		print(err)	

def info():
	print('\nThis Pydule is Created by D.Tamil Mutharasan \U0001F608\n')

def restr(oldstr,index,newstr):
	if isinstance(oldstr,str):
		new=''
		for i in range(len(oldstr)):
			if i==index:
				new+=newstr
			else:
				new+=oldstr[i]
		return new
	else:
		print(err)	

def relist(oldlist,index,newlist):
	if isinstance(oldlist,list):
		new=[]
		for i in range(len(oldlist)):
			if i==index:
				new+=[newlist]
			else:
				new+=[oldlist[i]]
		return new
	else:
		print(err)	

def retuple(oldtup,index,newtup):
	if isinstance(oldtup,tuple):
		new=tuple()
		for i in range(len(oldtup)):
			if i==index:
				new+=(newtup,)
			else:
				new+=(oldtup[i],)
		return new
	else:
		print(err)	

def clist(mx):
	List=[]
	print('Enter Values One by One \U0001F447\n')
	for i in range(mx):
		l=eval(input(f'Enter {i+1} Value :'))
		List.append(l)
	print('\nList Created Successfully \U00002714\n')
	return List

def ctuple(mx):
	Tuple=()
	print('Enter Values One by One \U0001F447\n')
	for i in range(mx):
		t=eval(input(f'Enter {i+1} Value :'))
		Tuple+=(t,)
	print('\nTuple Created Successfully \U00002714\n')
	return Tuple

def cdict(mx):
	Dict={}
	for i in range(mx):
		key=eval(input(f'Enter the Key of No.{i+1} Element :'))
		value=eval(input(f'Enter the Value of No.{i+1} Element :'))
		Dict[key]=value
	print('\nDictionary Created Successfully \U00002714')	
	return Dict

def cset(mx):
	Set=set()
	print('Enter Values One by One \U0001F447\n')
	for i in range(mx):
		s=eval(input(f'Enter {i+1} Values : '))
		Set.add(s)
	print('\nSet Created Successfully \U00002714')	
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
		print(err)

def open_app(app_name):
	try:
		open(app_name)
	except:
		print(err)	

def search(content):
	try:
		kt.search(content)	
		print('\nSearching \U0001F50E...\n')		
	except:
		print(err)	

def play_song(song_path):
	try:
		playsound(song_path)
	except:
		print(err)	

def restart_system():
	try:
		print('\nRestarting the System \U0001F4BB...\n')		
		os.system("shutdown /r /t 1")
	except:
		print(err)	

def shutdown_system():
	try:
		print('\nShutting Down Your System \U0001F4BB...\n')
		return os.system("shutdown /s /t 1")
	except:
		print(err)		

def todays_date():
	try:
		d=date.today()
		print(f"\nTodays Date is {d}\n")
	except:
		print(err)	

def time_now():
	try:
		now = datetime.now()
		current_time = now.strftime("%H:%M:%S %p")
		print(f"\nCurrent Time \U0001F55B : {current_time}\n")
	except:
		print(err)	

def say(content):	
	try:
		print('Converting text to Speech...') 
		engine.say(content)
		engine.runAndWait()  
	except:
		print(err)

def open_file(path):
	try:
		print('Opening...')
		os.startfile(path)
	except:
		print(err)		

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


		city = input("Enter the Name of the City \U0001F3D9 : ")
		city = city+" weather"
		weather(city)
	except:	
		print(err)

def set_voice(num):
	if num<=2:
		try:
			voices=engine.getProperty('voices')
			engine.setProperty('voice',voices[num].id)
		except:
			print(err)
	else:
		print('\n\u26A0 Voice Not Found \u26A0\n')		

def voice_rate(num):
	try:
		engine.setProperty('rate',num)
	except:
		print(err)				