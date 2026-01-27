# Advanced Voice Assistant

An intelligent voice assistant with natural language processing capabilities, capable of performing various tasks including sending emails, setting reminders, providing weather updates, controlling smart home devices, and answering general knowledge questions.

## Features

### 🎤 Voice Recognition
- Real-time speech-to-text conversion using Google Speech Recognition API
- Noise cancellation and ambient noise adjustment
- Timeout and phrase time limit handling

### 📧 Email Functionality
- Send emails via SMTP (Gmail, Outlook, etc.)
- Natural language email composition
- Automatic recipient and subject extraction

### ⏰ Reminder System
- Set reminders with specific times
- Relative time support (e.g., "in 30 minutes")
- Automatic notification system

### 🌤️ Weather Updates
- Real-time weather information via OpenWeatherMap API
- Support for multiple cities
- Temperature, humidity, wind speed, and conditions

### 🏠 Smart Home Control
- Framework for controlling smart home devices
- Turn devices on/off via voice commands
- Extensible for integration with Philips Hue, SmartThings, Home Assistant, etc.

### 📚 General Knowledge
- Answer questions using Wikipedia API
- Web search integration for additional information
- Natural language query processing

### 🕐 Time & Date
- Current time queries
- Date information
- Natural language time recognition

## Installation

### Windows (Recommended Method)

**Option 1: Use the provided installation script (Easiest)**
```bash
# Run the batch file
install_windows.bat

# Or use PowerShell
.\install_windows.ps1
```

**Option 2: Manual installation using pipwin**
```bash
pip install pipwin
pipwin install pyaudio
pip install -r requirements.txt
```

**Option 3: Install Visual C++ Build Tools**
1. Download and install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Then run: `pip install -r requirements.txt`

### Linux
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install -r requirements.txt
```

### macOS
```bash
brew install portaudio
pip install -r requirements.txt
```

### Alternative: Text Input Mode
If PyAudio installation fails, the assistant will automatically fall back to text input mode, allowing you to type commands instead of speaking them.

3. **Configure the assistant:**
   - Edit `config.json` and add your credentials:
     - **Email:** Add your SMTP server details and credentials
       - For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833)
     - **Weather:** Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
     - **OpenAI (Optional):** For enhanced AI capabilities

## Usage

Run the voice assistant:
```bash
python Voice_assist.py
```

### Example Commands

- **Greetings:** "Hello", "Hi", "Hey"
- **Email:** "Send email to john@example.com about meeting tomorrow"
- **Reminders:** "Set reminder to call mom at 3 PM" or "Remind me to buy groceries in 30 minutes"
- **Weather:** "What's the weather in New York?" or "Weather forecast"
- **Smart Home:** "Turn on the lights" or "Turn off the fan"
- **Questions:** "What is artificial intelligence?" or "Tell me about Python programming"
- **Time/Date:** "What time is it?" or "What's the date today?"
- **Exit:** "Goodbye", "Exit", "Quit"

## Configuration

### Email Setup (Gmail Example)

1. Enable 2-Step Verification on your Google Account
2. Generate an App Password:
   - Go to Google Account → Security → 2-Step Verification → App passwords
   - Generate a password for "Mail"
3. Update `config.json`:
   ```json
   "sender_email": "your_email@gmail.com",
   "sender_password": "your_16_character_app_password"
   ```

### Weather API Setup

1. Sign up at [OpenWeatherMap](https://openweathermap.org/api)
2. Get your free API key
3. Update `config.json`:
   ```json
   "weather": {
       "api_key": "your_api_key_here",
       "default_city": "YourCity"
   }
   ```

## Architecture

The assistant uses:
- **Intent Recognition:** Pattern matching with regex for natural language understanding
- **Entity Extraction:** Extracts relevant information (emails, times, locations) from commands
- **Modular Design:** Each feature is implemented as a separate method for easy extension
- **Threading:** Reminders run in background threads for non-blocking operation

## Extending the Assistant

### Adding New Intents

1. Add pattern to `intent_patterns` dictionary:
   ```python
   'new_intent': ['pattern1', 'pattern2']
   ```

2. Add entity extraction logic in `extract_entities()` method

3. Add handler in `process_command()` method

### Integrating Smart Home APIs

Modify the `control_smart_home()` method to integrate with your preferred platform:

```python
def control_smart_home(self, device: str, action: str):
    # Example: Philips Hue integration
    # hue_client = PhilipsHueClient()
    # hue_client.set_light(device, action)
    pass
```

## Troubleshooting

### Microphone Issues
- Ensure microphone permissions are granted
- Check microphone is working in system settings
- Try adjusting `adjust_for_ambient_noise` duration

### Speech Recognition Errors
- Check internet connection (uses Google Speech Recognition API)
- Speak clearly and reduce background noise
- Increase timeout if needed

### Email Sending Fails
- Verify SMTP credentials in config.json
- For Gmail, ensure App Password is used (not regular password)
- Check firewall/network settings

## Requirements

- Python 3.7+
- Microphone
- Internet connection (for speech recognition and APIs)
- API keys for weather and email services

## License

This project is part of OIBSIP internship tasks.

## Future Enhancements

- [ ] Integration with OpenAI GPT for more intelligent responses
- [ ] Calendar integration for scheduling
- [ ] Music playback control
- [ ] News updates
- [ ] Translation capabilities
- [ ] Multi-language support
- [ ] Voice cloning for personalized responses
