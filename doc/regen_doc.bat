@echo on
dir .\automation_framework | find "source"   
if %errorlevel%==0 goto ok        REM--if exist jump to :ok
if %errorlevel%==1 goto end       REM--if not exist jump to:end
:ok
rd /s /q "automation_framework\source"
rem del /f /a /q /s "automation_framework\source" rem clean content, keep directory structure
:end
echo end

sphinx-apidoc -o automation_framework/source .. --separate
call make clean
call make html
pause

