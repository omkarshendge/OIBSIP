import speech_recognition as sr
import pyttsx3
import datetime
import threading
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import re
from typing import Dict, List, Optional, Tuple
import wikipedia
import webbrowser

# Check if PyAudio is available (required for microphone input)
try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False
    print("Warning: PyAudio is not installed. Microphone input will not work.")
    print("To install PyAudio on Windows, run: pip install pipwin && pipwin install pyaudio")
    print("Or use the install_windows.bat script provided.")


class VoiceAssistant:
    def __init__(self):
        """Initialize the advanced voice assistant with all capabilities."""
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.reminders = []
        self.config = self.load_config()
        
        # Set up voice properties
        voices = self.engine.getProperty('voices')
        if voices:
            self.engine.setProperty('voice', voices[0].id)
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        
        # Initialize NLP patterns for intent recognition
        self.intent_patterns = {
            'email': ['send email', 'email to', 'mail to', 'send mail'],
            'reminder': ['set reminder', 'remind me', 'reminder for', 'set a reminder'],
            'weather': ['weather', 'temperature', 'forecast', 'how is the weather'],
            'smart_home': ['turn on', 'turn off', 'switch', 'control', 'smart home'],
            'question': ['what is', 'who is', 'tell me about', 'explain', 'what are'],
            'time': ['what time', 'current time', 'what is the time'],
            'date': ['what date', 'today date', 'what is the date'],
            'greeting': ['hello', 'hi', 'hey', 'good morning', 'good afternoon'],
            'goodbye': ['goodbye', 'bye', 'see you', 'exit', 'quit']
        }
        
        print("Voice Assistant initialized successfully!")
        self.speak("Hello! I'm your advanced voice assistant. How can I help you today?")
    
    def load_config(self) -> Dict:
        """Load configuration from config.json file."""
        config_file = os.path.join(os.path.dirname(__file__), 'config.json')
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        else:
            # Default configuration
            default_config = {
                'email': {
                    'smtp_server': 'smtp.gmail.com',
                    'smtp_port': 587,
                    'sender_email': '',
                    'sender_password': ''
                },
                'weather': {
                    'api_key': '',
                    'default_city': 'London'
                },
                'openai': {
                    'api_key': ''
                }
            }
            self.save_config(default_config)
            return default_config
    
    def save_config(self, config: Dict):
        """Save configuration to config.json file."""
        config_file = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)
    
    def speak(self, text: str):
        """Convert text to speech."""
        print(f"Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self) -> Optional[str]:
        """Listen for voice input and convert to text."""
        if not PYAUDIO_AVAILABLE:
            print("PyAudio is not installed. Please install it to use microphone input.")
            print("Windows: pip install pipwin && pipwin install pyaudio")
            # Fallback to text input for testing
            command = input("Enter command (text mode): ").strip()
            return command.lower() if command else None
        
        try:
            with sr.Microphone() as source:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                try:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    command = self.recognizer.recognize_google(audio)
                    print(f"You said: {command}")
                    return command.lower()
                except sr.WaitTimeoutError:
                    print("No speech detected.")
                    return None
                except sr.UnknownValueError:
                    print("Sorry, I did not understand that.")
                    return None
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
                    return None
        except OSError as e:
            print(f"Microphone error: {e}")
            print("Falling back to text input mode...")
            command = input("Enter command (text mode): ").strip()
            return command.lower() if command else None
    
    def recognize_intent(self, command: str) -> Tuple[str, Dict]:
        """Use NLP to recognize user intent from command."""
        command_lower = command.lower()
        
        # Check each intent pattern
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if pattern in command_lower:
                    return intent, self.extract_entities(intent, command)
        
        # Default to question if no specific intent found
        return 'question', {'query': command}
    
    def extract_entities(self, intent: str, command: str) -> Dict:
        """Extract relevant entities from the command based on intent."""
        entities = {}
        
        if intent == 'email':
            # Extract email address
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            email_match = re.search(email_pattern, command)
            if email_match:
                entities['recipient'] = email_match.group()
            
            # Extract subject
            subject_patterns = [r'subject[:\s]+([^,]+)', r'about[:\s]+([^,]+)']
            for pattern in subject_patterns:
                match = re.search(pattern, command, re.IGNORECASE)
                if match:
                    entities['subject'] = match.group(1).strip()
                    break
            
            # Extract message
            message_patterns = [r'message[:\s]+(.+)', r'say[:\s]+(.+)', r'tell[:\s]+(.+)']
            for pattern in message_patterns:
                match = re.search(pattern, command, re.IGNORECASE)
                if match:
                    entities['message'] = match.group(1).strip()
                    break
        
        elif intent == 'reminder':
            # Extract time
            time_patterns = [
                r'at\s+(\d{1,2}:\d{2})',
                r'at\s+(\d{1,2})\s*(?:am|pm)',
                r'in\s+(\d+)\s*(?:minutes?|hours?|mins?|hrs?)'
            ]
            for pattern in time_patterns:
                match = re.search(pattern, command, re.IGNORECASE)
                if match:
                    entities['time'] = match.group(1)
                    break
            
            # Extract reminder text
            reminder_keywords = ['remind me to', 'reminder for', 'about']
            for keyword in reminder_keywords:
                if keyword in command.lower():
                    parts = command.lower().split(keyword)
                    if len(parts) > 1:
                        entities['text'] = parts[1].strip()
                        break
        
        elif intent == 'weather':
            # Extract location
            location_patterns = [
                r'in\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
                r'for\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
                r'at\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
            ]
            for pattern in location_patterns:
                match = re.search(pattern, command)
                if match:
                    entities['location'] = match.group(1)
                    break
        
        elif intent == 'smart_home':
            # Extract device and action
            if 'turn on' in command.lower():
                entities['action'] = 'on'
                device = command.lower().replace('turn on', '').strip()
                entities['device'] = device
            elif 'turn off' in command.lower():
                entities['action'] = 'off'
                device = command.lower().replace('turn off', '').strip()
                entities['device'] = device
        
        elif intent == 'question':
            entities['query'] = command
        
        return entities
    
    def send_email(self, recipient: str, subject: str, message: str) -> bool:
        """Send an email using SMTP."""
        try:
            smtp_server = self.config['email']['smtp_server']
            smtp_port = self.config['email']['smtp_port']
            sender_email = self.config['email']['sender_email']
            sender_password = self.config['email']['sender_password']
            
            if not sender_email or not sender_password:
                self.speak("Email configuration is not set up. Please configure your email in config.json")
                return False
            
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))
            
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            
            self.speak(f"Email sent successfully to {recipient}")
            return True
        except Exception as e:
            self.speak(f"Failed to send email: {str(e)}")
            return False
    
    def set_reminder(self, reminder_text: str, reminder_time: str):
        """Set a reminder that will notify at the specified time."""
        try:
            # Parse time
            if ':' in reminder_time:
                hour, minute = map(int, reminder_time.split(':'))
            elif 'in' in reminder_time.lower():
                # Relative time
                numbers = re.findall(r'\d+', reminder_time)
                if numbers:
                    minutes = int(numbers[0])
                    reminder_datetime = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
                    hour = reminder_datetime.hour
                    minute = reminder_datetime.minute
                else:
                    self.speak("I couldn't understand the time. Please specify time clearly.")
                    return
            else:
                self.speak("I couldn't understand the time format.")
                return
            
            reminder_datetime = datetime.datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
            if reminder_datetime < datetime.datetime.now():
                reminder_datetime += datetime.timedelta(days=1)
            
            reminder = {
                'text': reminder_text,
                'datetime': reminder_datetime,
                'notified': False
            }
            self.reminders.append(reminder)
            
            self.speak(f"Reminder set for {reminder_datetime.strftime('%I:%M %p')} to {reminder_text}")
            
            # Start reminder check thread
            threading.Thread(target=self.check_reminders, daemon=True).start()
        except Exception as e:
            self.speak(f"Failed to set reminder: {str(e)}")
    
    def check_reminders(self):
        """Check and notify about due reminders."""
        while True:
            now = datetime.datetime.now()
            for reminder in self.reminders:
                if not reminder['notified'] and now >= reminder['datetime']:
                    self.speak(f"Reminder: {reminder['text']}")
                    reminder['notified'] = True
            threading.Event().wait(60)  # Check every minute
    
    def get_weather(self, location: Optional[str] = None) -> str:
        """Get weather information for a location."""
        try:
            api_key = self.config['weather']['api_key']
            if not api_key:
                return "Weather API key is not configured. Please add your OpenWeatherMap API key to config.json"
            
            city = location or self.config['weather']['default_city']
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                temp = data['main']['temp']
                description = data['weather'][0]['description']
                humidity = data['main']['humidity']
                wind_speed = data['wind']['speed']
                
                weather_info = f"The weather in {city} is {description}. Temperature is {temp} degrees Celsius. Humidity is {humidity} percent and wind speed is {wind_speed} meters per second."
                self.speak(weather_info)
                return weather_info
            else:
                error_msg = f"Could not fetch weather data. Error code: {response.status_code}"
                self.speak(error_msg)
                return error_msg
        except Exception as e:
            error_msg = f"Failed to get weather: {str(e)}"
            self.speak(error_msg)
            return error_msg
    
    def answer_question(self, query: str) -> str:
        """Answer general knowledge questions using Wikipedia."""
        try:
            # Clean query
            query = query.replace('what is', '').replace('who is', '').replace('tell me about', '').strip()
            
            # Try Wikipedia search
            try:
                summary = wikipedia.summary(query, sentences=2)
                self.speak(summary)
                return summary
            except wikipedia.exceptions.DisambiguationError as e:
                # If disambiguation, use first option
                summary = wikipedia.summary(e.options[0], sentences=2)
                self.speak(summary)
                return summary
            except wikipedia.exceptions.PageError:
                # If Wikipedia fails, try web search
                search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                self.speak(f"I couldn't find specific information. Let me search the web for you.")
                webbrowser.open(search_url)
                return "Opening web search results."
        except Exception as e:
            error_msg = f"Sorry, I couldn't answer that question: {str(e)}"
            self.speak(error_msg)
            return error_msg
    
    def control_smart_home(self, device: str, action: str):
        """Control smart home devices (simulated)."""
        # This is a framework for smart home control
        # In a real implementation, you would integrate with actual smart home APIs
        # like Philips Hue, SmartThings, Home Assistant, etc.
        
        action_text = "turn on" if action == "on" else "turn off"
        response = f"I would {action_text} the {device} now. Note: This is a simulated response. To control actual devices, integrate with your smart home platform's API."
        self.speak(response)
        
        # Example: Log the command (in real implementation, send API request)
        print(f"[Smart Home] Command: {action_text} {device}")
        return response
    
    def get_time(self) -> str:
        """Get current time."""
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.speak(f"The current time is {current_time}")
        return current_time
    
    def get_date(self) -> str:
        """Get current date."""
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        self.speak(f"Today's date is {current_date}")
        return current_date
    
    def process_command(self, command: str):
        """Process a command based on recognized intent."""
        if not command:
            return
        
        intent, entities = self.recognize_intent(command)
        
        if intent == 'greeting':
            greetings = ["Hello! How can I help you?", "Hi there! What can I do for you?", "Hey! Ready to assist."]
            self.speak(greetings[hash(command) % len(greetings)])
        
        elif intent == 'goodbye':
            self.speak("Goodbye! Have a great day!")
            return False
        
        elif intent == 'email':
            recipient = entities.get('recipient')
            subject = entities.get('subject', 'No Subject')
            message = entities.get('message', '')
            
            if not recipient:
                self.speak("I need an email address. Please say the recipient's email address.")
                recipient_command = self.listen()
                if recipient_command:
                    email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', recipient_command)
                    if email_match:
                        recipient = email_match.group()
            
            if not message:
                self.speak("What message would you like to send?")
                message = self.listen() or ""
            
            if recipient:
                self.send_email(recipient, subject, message)
            else:
                self.speak("I couldn't find a valid email address. Please try again.")
        
        elif intent == 'reminder':
            reminder_text = entities.get('text', 'Reminder')
            reminder_time = entities.get('time', '')
            
            if not reminder_time:
                self.speak("What time should I set the reminder for?")
                reminder_time = self.listen() or ""
            
            if reminder_time:
                self.set_reminder(reminder_text, reminder_time)
            else:
                self.speak("I couldn't understand the time. Please try again.")
        
        elif intent == 'weather':
            location = entities.get('location')
            self.get_weather(location)
        
        elif intent == 'smart_home':
            device = entities.get('device', 'device')
            action = entities.get('action', 'on')
            self.control_smart_home(device, action)
        
        elif intent == 'question':
            query = entities.get('query', command)
            self.answer_question(query)
        
        elif intent == 'time':
            self.get_time()
        
        elif intent == 'date':
            self.get_date()
        
        else:
            self.speak("I'm not sure how to help with that. Could you rephrase?")
        
        return True
    
    def run(self):
        """Main loop for the voice assistant."""
        print("\n" + "="*50)
        print("Advanced Voice Assistant")
        print("Say 'goodbye' or 'exit' to quit")
        print("="*50 + "\n")
        
        while True:
            try:
                command = self.listen()
                if command:
                    if not self.process_command(command):
                        break
            except KeyboardInterrupt:
                self.speak("Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
                self.speak("Sorry, an error occurred. Please try again.")


def main():
    """Main entry point."""
    assistant = VoiceAssistant()
    assistant.run()


if __name__ == "__main__":
    main()
