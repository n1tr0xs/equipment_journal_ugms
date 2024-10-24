@echo off

:loop
manage.py runserver 10.55.0.100:2410
goto loop

pause