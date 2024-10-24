@echo off

:loop
manage.py runserver --insecure --force-color 10.55.0.100:2410
goto loop

pause