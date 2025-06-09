@echo off
echo Dang khoi dong ung dung...

start cmd /k "cd %~dp0backend\manageAirport && python manage.py runserver"
start cmd /k "cd %~dp0frontend && ng serve --open"

echo Da khoi dong ca backend va frontend!
echo Backend: http://127.0.0.1:8000
echo Frontend: http://localhost:4200 