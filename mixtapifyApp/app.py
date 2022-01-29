#!/usr/bin/env python3

# kivy module
import kivy
from kivy.app import App
from kivy.uix.label import Label

# app
class mixtapify(App):
	def build(self):
		return Label(text="Les intérêts gagnés après 72 jours sont: \n La valeur acquise après 72 jours est: ")
	
	
	
if __name__ == "__main__":
	mixtapify().run()