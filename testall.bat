set BASEPATH=C:\gis
set PROPY=c:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe
set OGPYTHONPATH=%PYTHONPATH%
set PYTHONPATH=%BASEPATH%\geodatabase-buildings-automation\src\py;%PYTHONPATH%
CALL %PROPY% .\src\py\test-featureclassrules.py
set PYTHONPATH=%OGPYTHONPATH%
