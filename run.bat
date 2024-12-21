@echo off
set PYTHONPATH=%PYTHONPATH%;%~dp0src
cd src/frontend
streamlit run app.py
cd ../.. 