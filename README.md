# OmniVista Core Licenses


Get the number of core licenses from each stack using the OmniVista API. This can be useful for network admins who want to know how many switches are currently online in a stack.

## How to use:

Get the number of core licenses for 10.0.0.1:
<code>python corelicense.py 10.0.0.1</code>


Get the number of core licenses for 10.0.0.1 and outputting it:
<code>python corelicense.py 10.0.0.1 -output</code>


Get the number of core licenses for a list of IP addresses from a .txt file:
<code>python corelicense.py ip_list.txt</code>


Get the number of core licenses for a list of IP addresses and outputting it:
<code>python corelicense.py ip_list.txt -output</code>

*<b>.txt files must have one IP address per a line</b>*

