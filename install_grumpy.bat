@echo off
set env_name=grumpy_env
rem cd ..\

@echo Creation of Grumpy Virtual Environment
python -m venv %env_name%

@echo Grumpy Virtual Environments successfully created
@echo Next step: installing dependencies

call .\%env_name%\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
call .\%env_name%\Scripts\deactivate.bat

@echo Grumpy dependencies successfully installed and updated

@pause