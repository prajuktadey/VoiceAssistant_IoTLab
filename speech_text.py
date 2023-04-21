#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import speech_recognition as sr
r = sr.Recognizer()

with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    print("Speak now.")
    audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print("You said: ", text)
    except sr.UnknownValueError:
        print("Sorry, could not understand your speech.")
    except sr.RequestError as e:
        print("Request error; {0}".format(e))

