how to use Python sensor to detect Palo Alto Power supplies
there are two brief infomation of Power Supplies status on Palo Alto platform, one is the insert status and the other is alarm status.
for 5200 series and 220 series, or saying the low and medium end, there are no SNMP mib for it. looks like the only option is using some cli commands to retrieve the info. But  based on the result we got during testing, Palo Alto platform don't support direct ssh command without interactive loging. lucky, there is a PaloAlto SDK is available.
pan-os-python:https://github.com/PaloAltoNetworks/pan-os-python

In order to use it, some preparation is needed:
1. PRTG Python using its own runing time, here is a way to install new module for it
KB:https://kb.paessler.com/en/topic/84447-add-python-modules
Download https://bootstrap.pypa.io/get-pip.py into PRTGs python directory
cd C:\Program Files (x86)\PRTG Network Monitor\python\
python.exe get-pip.py
cd Scripts
pip install google-api-python-client

especially, if you are using a enterprise MA-account, if you install the new module with your account, the new module will be added to the windows roaming folder, which cannot be recognized by PRTG. you need a local account directly on PRTG server to install the new module

2.add the python script in following folder PRTG root\Custom Sensors\python\
3.add a read-admin role in PaloAlto appliance, add it to PRTG credential. in this script, I use Linux user for PaloAlto.
4.add a python sensor for the PaloAlto host.

About alarm:
alarm trigger is defined in the script as "limit_min/max_error"
when power supply not in place (insert status is 0) or has alarm (alarm status is 1), alarm will be triggered
