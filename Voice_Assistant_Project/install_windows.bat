@echo off
echo Installing Voice Assistant Dependencies for Windows...
echo.

REM Install pipwin if not already installed
pip install pipwin

REM Install PyAudio using pipwin (pre-built wheels)
pipwin install pyaudio

REM Install other dependencies
pip install SpeechRecognition==3.10.0
pip install pyttsx3==2.90
pip install requests==2.31.0
pip install wikipedia==1.4.0

echo.
echo Installation complete!
echo.
pause
