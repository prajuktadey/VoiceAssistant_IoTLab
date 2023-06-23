#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pyttsx3

mytext = 'Hello, how are you?'
engine = pyttsx3.init()

engine.setProperty('rate', 150)  # Set the speaking rate in words per minute
engine.setProperty('voice', 'english')  # Set the voice

engine.say(mytext)
engine.runAndWait()

