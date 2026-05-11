@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo مجلد المشروع: %CD%
echo.
python app.py
if errorlevel 1 (
  echo.
  echo فشل التشغيل. جرب: py app.py
  pause
)
