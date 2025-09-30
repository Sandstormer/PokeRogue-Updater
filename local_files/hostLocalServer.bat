@REM This script creates a local server for mobile debugging
@REM It shows you the local IP address of the server, port 8000

@echo off
setlocal enabledelayedexpansion
for /f "tokens=2 delims=:" %%A in ('ipconfig ^| findstr "IPv4 Address"') do (
    set IP=%%A
    set IP=!IP:~1!
)
echo Your local IP address is !IP!
echo The website will be accessible at !IP!:8000
echo .
echo Use Firefox Mobile Debugging at about:debugging#/setup
echo .
echo The local server will launch . . .
pause
echo .
echo The local server is live
cd website
python -m http.server 8000 --bind 0.0.0.0