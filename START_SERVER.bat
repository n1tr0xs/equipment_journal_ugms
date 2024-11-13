@echo off

:loop
manage.py runserver --insecure --force-color 127.0.0.1:2410
goto loop

pause