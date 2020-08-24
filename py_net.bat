@echo OFF
REM	We need to run Python as a 32 bit application, which requires
REM	that we launch it from a 32 bit command prompt on 64 bit windows.

set FWVersion=8
call ..TELibs\Python27.NET\FW%FWVersion%\python32.exe
