# Usage
1. Set your php or other enviroments to config.properties
2. Get phpggc
``` bash
cd libs
git clone https://github.com/ambionics/phpggc 
```
3. Get ysoserial
``` bash
wget https://github.com/frohoff/ysoserial/releases/download/v0.0.6/ysoserial-all.jar
```
4. Install requirements
``` bash
python3 -m pip install -r requirements.txt
```
1. Run?
``` bash
python3 main.py
```
1. Have fun.

# Now avaliable exps
|Name|Type|Products|Update Time|
|---|---|---|---|
|e-office v10 auth-file|RCE|Ecology_E_Office_v10|Apr.14,2024|
|NC-ConfigResourceServlet-Deserialization|RCE|UFIDA_NC65|Apr.15,2024|
|NC-NCEmessage-Deserialization|RCE|UFIDA_NC65|Apr.16,2024|

# Declare
To use these tools, you must comply with local legal regulations, or authorized. The losses incurred are not related to the implementation of this repository.

# Changelog
|Changes|Datetime|
|---|---|
|Rebuild to modules applications|16.Apr,2024|
|Init|14.Apr,2024|