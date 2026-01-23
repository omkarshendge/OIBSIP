import pandas as pd

import speech_recognition as sr 
class VoiceAssistant:
    def __init__(self, data_file):
        self.data = pd.read_csv(data_file)
        self.recognizer = sr.Recognizer()

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
            try:
                command = self.recognizer.recognize_google(audio)
                print(f"Recognized command: {command}")
                return command
            except sr.UnknownValueError:
                print("Sorry, I did not understand that.")
                return None
            except sr.RequestError:
                print("Could not request results; check your network connection.")
                return None

    def respond(self, command):
        if command:
            response = self.data[self.data['command'] == command]['response']
            if not response.empty:
                print(f"Response: {response.values[0]}")
            else:
                print("Sorry, I don't have a response for that command.")
  