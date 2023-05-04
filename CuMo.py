#imports
import pyttsx3
import speech_recognition as sr
from random import *
from datetime import datetime
import requests, json
from googlesearch import search
import wolframalpha

#init 
s = pyttsx3.init()
r = sr.Recognizer()

#variables
weatherAPI = "8dbe7db64bace3ea06d18d575705b40e"
weatherURL = "http://api.openweathermap.org/data/2.5/weather?"
wolframID = "WQAQ26-99WH7883W4"

#Set voice - MSHazel
voices = s.getProperty('voices')
s.setProperty('voice', voices[0].id)


#functions                                                  
def say(text):
	s.say(text)
	s.runAndWait()
	
	
def greeting():
    greeting = ["Hi i'm QueueMo your voice assistant","Hello there i'm QueueMo your voice assistant","Hola soy QueueMo tes voices assistante"]
    s.say(choice(greeting))
    s.runAndWait()
	

def shutdown():
	say("Shutting down")
	s.stop()
	raise Exception ("Shutdown")

def curTime():
	now = datetime.now()
	current_time = now.strftime("%H %M")
	say(("The time is",current_time))

def setTimer(text):
	if "minutes" in text:
		
		time = 1
	say("Setting timer for",time,"mins")

def curWeather(city):

	complete_url = weatherURL + "appid=" + weatherAPI + "&q=" + city
	response = requests.get(complete_url)
	x = response.json()
	if (x["cod"] != "404"):
		y = x["main"]
		temp = y["temp"]
		humidity = y["humidity"]
		z = x["weather"]
		description = z[0]["description"]
		say(("In",city,"the current temperature is",round(temp-273,0),"degrees with a humidity of",humidity,"percent","The weather is currently",description))

	
def menu(text):
	done = False
	if "hello" in text or "hi" in text:
		done = True
		greeting()
		
	if "what" in text and "time" in text:
		done = True
		curTime()
		
	
	if "what" in text and "weather" in text:
		done = True
		if "in" in text:
			location = text.index("in")
			city = text[location+2:]
			curWeather(city)
			print(city)

		elif "in" not in text:
			say("In what city")
			audio2 = r.listen(source2)	
			city = r.recognize_google(audio2)
			curWeather(city)
	

	if "what" in text and done == False:
		done = True
		query = str(text)
		try:
			client = wolframalpha.Client(wolframID)
			res = client.query(query)
			answer = next(res.results).text
  
			say(answer)
		except:
			for j in search(query, tld="co.in", num=10, stop=10, pause=2):
				print(j)
		

	if ("shut" in text and "down" in text) or ("shutdown" in text) and done == False:
		shutdown()
	
	elif done == False:
		say("Hmm not sure about that")
    

	
menu(input("B: "))
#greeting()

while True:

	try:
		with sr.Microphone() as source2:
			r.adjust_for_ambient_noise(source2, duration=0.3)
			print("listening")
			audio2 = r.listen(source2)
			
			MyText = r.recognize_google(audio2)
			MyText = MyText.lower()
			print(MyText)
			#if "CuMo" in MyText:
			menu(MyText)
			
	except sr.RequestError as e:
		print("Could not request results; {0}".format(e))
		
	except sr.UnknownValueError:
		print("unknown error occurred")
		
