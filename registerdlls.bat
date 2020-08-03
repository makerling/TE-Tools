@echo OFF
for /r %i in (*.dll) do @echo %~ni

REM dir "C:\Program Files (x86)\SIL\FieldWorks 8" *.dll