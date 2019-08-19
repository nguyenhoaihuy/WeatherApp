import tkinter as tk
from tkinter import *
import tkinter.messagebox as tkb
import requests as rq
from PIL import ImageTk, Image
from io import BytesIO

HEIGHT = 500
WIDTH = 600

#Read file line by line and return a dictionary
def readFile(filename):
	dic = []
	f = open(filename, "r")
	lines = f.readlines()
	for line in lines:
		line = line.replace('\n', '')
		dic.append(line)
	return dic

city_id = readFile('cities.txt') #read file name cities which store current added cities code

#Write into a file from the city_id list
def writeFile(filename):
	f = open(filename, "w")
	for line in city_id:
		f.write(line+"\n")

root = tk.Tk()
var = IntVar()
var.set(1)

# api.openweathermap.org/data/2.5/weather?q=London
# this function call apis from openweathermap.org
def get_weather(location, option, bycity):
	url = "https://api.openweathermap.org/data/2.5/weather"
	key = '[your key here]'
	if (option==2):
		url = "https://api.openweathermap.org/data/2.5/forecast"

	params = {'APPID': key, 'id': location, 'units':'imperial'}
	if (bycity): # if choose option search by name of city
		params = {'APPID': key, 'q': location, 'units':'imperial'}
	response = rq.get(url, params=params)
	return response.json()

# check if the city code exists in the current list or not
def isExisting(city):
	for each in city_id:
		if (each==city):
			return TRUE
	return FALSE

def showWeatherCallBack(location, option):
	clear() # clear the show area before show other data
	response = get_weather(location, option, 1)
	
	if (option==1):
		added=FALSE
		if (isExisting(response['id'])):
			added=TRUE
		showCurrentWeather(response, added, 5)
	if (option==2):
		print(response)
		showForecastWeather(response)

#show 5 days forecast with a particular response
def showForecastWeather(response):
	position = 5
	list_num = 4
	for i in range(0,5):
		row = Frame(show, bg='#c2d9ff')
		row.place(relx=0, y=position, relwidth=1, height=40)

		# show information
		Label(row, text=response['city']['name'], bg="#c2d9ff", anchor='w').place(x=5, y=5,relwidth=0.2, height=25)
		Label(row, text=response['list'][list_num]['weather'][0]['description'], bg="#c2d9ff", anchor='w').place(relx=0.22, y=5,relwidth=0.3, height=25)
		Label(row, text=str(response['list'][list_num]['main']['temp'])+" F", bg="#c2d9ff", anchor='w').place(relx=0.45, y=5,relwidth=0.2, height=25)
		Label(row, text=response['list'][list_num]['dt_txt'], bg="#c2d9ff", anchor='w').place(relx=0.6, y=5,relwidth=0.2, height=25)
		# http://openweathermap.org/img/wn/10d@2x.png
		# show icon of weather
		load = Image.open('./icon/'+response['list'][list_num]['weather'][0]['icon']+'@2x.png')
		load = load.resize((50,50), Image.ANTIALIAS)
		render = ImageTk.PhotoImage(load)
		img = Label(row, image=render, bg="#c2d9ff")
		img.image = render
		img.place(relx=0.8, y=5,relwidth=0.1, height=30)

		#increasement of the loop
		position += 45
		list_num+=8

# show current weather with a particular response
def showCurrentWeather(response, added, position):
	addState=NORMAL
	deleteState=DISABLED 
	if (added):
		addState=DISABLED
		deleteState=NORMAL 
	row = Frame(show, bg='#c2d9ff')
	row.place(relx=0, y=position, relwidth=1, height=40)
	Label(row, text=response['name'], bg="#c2d9ff", anchor='w').place(x=5, y=5,relwidth=0.2, height=25)
	Label(row, text=response['weather'][0]['description'], bg="#c2d9ff", anchor='w').place(relx=0.22, y=5,relwidth=0.3, height=25)
	Label(row, text=str(response['main']['temp'])+" F", bg="#c2d9ff", anchor='w').place(relx=0.45, y=5,relwidth=0.2, height=25)
	# http://openweathermap.org/img/wn/10d@2x.png
	
	# show icon of weather
	load = Image.open('./icon/'+response['weather'][0]['icon']+'@2x.png')
	load = load.resize((50,50), Image.ANTIALIAS)
	render = ImageTk.PhotoImage(load)
	img = Label(row, image=render, bg="#c2d9ff")
	img.image = render
	img.place(relx=0.60, y=5,relwidth=0.1, height=30)

	# button add and delete
	Button(row, text="add", command=lambda: addCallBack(response['id']), state=addState, width=10, bg='#00cf0a').place(relx=0.75, y=5,relwidth=0.1, height=25)
	Button(row, text="delete", command=lambda: deleteCallBack(response['id']), state=deleteState, width=10, bg='#ff3721').place(relx=0.87, y=5,relwidth=0.1, height=25)

# preload when start the app 
def preloadData():
	y=5
	for city in city_id: #the city_id list is created above by call read function
		response = get_weather(city, 1, 0)
		showCurrentWeather(response,1,y)
		y+=45

# add a given city code into the city_id and write back to the file cities.txt, then clear and reload it
def addCallBack(city):
	if (not isExisting(str(city))):
		city_id.append(str(city))
	writeFile('cities.txt')
	clear()
	preloadData()

# delete a selected city from the city_id list and write back to the file cities.txt, then clear and reload it
def deleteCallBack(city):
	if (isExisting(str(city))):
		city_id.remove(str(city))
	print(city_id)
	writeFile('cities.txt')
	clear()
	preloadData()

# clear the show area
def clear():
	for child in show.winfo_children():
		child.destroy()

# initialize a canvas
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg='white')
canvas.pack()

# initialize a background lay over the canvas
background_image = Image.open('cloudy-sky.jpg')
render = ImageTk.PhotoImage(background_image)
background_label = Label(root, image=render, bg="white")
background_label.image = render
background_label.place(relwidth=1, relheight=1)


control = tk.Frame(root, bg='#011d4d')
control.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.3)

show = tk.Frame(root, bg='#011d4d')
show.place(relx=0.05, rely=0.37, relwidth=0.9, relheight=0.5)

button_area = tk.Frame(control, bg='#c2d9ff')
button_area.place(relx=0.7, rely=0.05, relwidth=0.27, relheight=0.9)

entry_area = tk.Frame(control, bg='#c2d9ff')
entry_area.place(relx=0.03, rely=0.05, relwidth=0.64, relheight=0.9)

location_label = tk.Label(entry_area, text="Location", bg='#c2d9ff')
location_label.place(x=5, y=5, width=50, height=20)

entry_location = tk.Entry(entry_area,  highlightthickness=2)
entry_location.place(relx=0.05, y=30, relwidth=0.9, height=30)

option_area = tk.Frame(entry_area, bg='#c2d9ff')
option_area.place(relx=0.05, y=70, relwidth=0.9, relheight=.5)

Radiobutton(option_area, text="Current Weather", variable=var, value=1, bg='#c2d9ff').pack(anchor='w')
Radiobutton(option_area, text="3 days forecast", variable=var, value=2, bg='#c2d9ff').pack(anchor='w')

button = tk.Button(button_area, text = "Show Weather", command=lambda: showWeatherCallBack(entry_location.get(), var.get()))
button.place(relx=0.05, rely=0.35, relwidth=0.9, relheight=0.3)

clear_button = tk.Button(root, text = "clear", command=clear)
clear_button.place(relx=0.45, rely=0.9, relwidth=0.1, height=30)

preloadData()


root.mainloop()

