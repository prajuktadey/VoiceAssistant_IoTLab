#!/usr/bin/env python
# coding: utf-8

# In[4]:


import requests
from bs4 import BeautifulSoup
import pyttsx3
import speech_recognition as sr
import datetime
import json

import openai
openai.api_key = "YOUR KEY"


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak:")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        # said = ""
        said = r.recognize_google(audio)

        try:
            print("You said: \n" + said)
        except sr.UnknownValueError:
            print("Sorry, could not understand your speech.")
        except sr.RequestError as e:
            print("Request error; {0}".format(e))

    return said.lower()


def query(user_query):
    url = "https://www.google.co.in/search?q=" + user_query
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(class_='Z0LcW t2b5Cf').get_text()
    print(results)
    return results


def chatgpt(user_query):
    response = openai.Completion.create(engine='text-davinci-003',
                                        prompt=user_query,
                                        n=1,
                                        temperature=0.5,
                                        max_tokens=50,
                                        top_p=1)
    return response['choices'][0]['text']


def get_date_time():
    now = datetime.datetime.now()
    date = now.strftime("%A, %B %d, %Y")
    time = now.strftime("%I:%M %p")
    return "The date is " + date + " and the time is " + time


def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=YOUR_KEY&units=metric"
    response = requests.get(url)
    data = json.loads(response.text)
    if data["cod"] == "404":
        return "Sorry, the city was not found."
    else:
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        return f"The weather in {city} is {weather_description}. The temperature is {temperature}°C. The humidity is {humidity}%. The wind speed is {wind_speed} m/s."


WAKE = "hello"
speak("Active")

while True:
    print("Active")
    # speak("Active")
    texts = get_audio()

    if texts.count(WAKE) > 0:
        print("I am listening")
        speak("I am listening")
        try:
            var = get_audio()
            if "date" in var or "time" in var:
                speak(get_date_time())
            elif "weather" in var:
                city = var.split("in")[-1].strip()
                speak(get_weather(city))
            else:
                # result = query(var)
                result = chatgpt(var)
                print(result)
                speak(result)
        except Exception:
            # print('Sorry no result')
            speak('Sorry no results.')

