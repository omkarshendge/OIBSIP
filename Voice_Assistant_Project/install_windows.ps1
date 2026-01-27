# PowerShell script to install Voice Assistant dependencies on Windows
Write-Host "Installing Voice Assistant Dependencies for Windows..." -ForegroundColor Green
Write-Host ""

# Install pipwin if not already installed
Write-Host "Installing pipwin..." -ForegroundColor Yellow
pip install pipwin

# Install PyAudio using pipwin (pre-built wheels)
Write-Host "Installing PyAudio..." -ForegroundColor Yellow
pipwin install pyaudio

# Install other dependencies
Write-Host "Installing other dependencies..." -ForegroundColor Yellow
pip install SpeechRecognition==3.10.0
pip install pyttsx3==2.90
pip install requests==2.31.0
pip install wikipedia==1.4.0

Write-Host ""
Write-Host "Installation complete!" -ForegroundColor Green
Write-Host ""
