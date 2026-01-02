@echo off
set env_name=.grumpy_env
rem cd ..\

call .\%env_name%\Scripts\activate.bat
python main.py
call .\%env_name%\Scripts\deactivate.bat
