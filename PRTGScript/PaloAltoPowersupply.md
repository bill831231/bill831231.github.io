how to use Python sensor to detect Palo Alto Power supplies
there are two brief infomation of Power Supplies status on Palo Alto platform, one is the insert status and the other is alarm status.
for 5200 series and 220 series, or saying the low and medium end, there are no SNMP mib for it. looks like the only option is using some cli commands to retrieve the info. But  based on the result we got during testing, Palo Alto platform don't support direct ssh command without interactive loging. lucky, there is a PaloAlto SDK is available.
pan-os-python:https://github.com/PaloAltoNetworks/pan-os-python

In order to use it, some preparation is needed:


