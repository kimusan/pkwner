```
██████╗ ██╗  ██╗██╗    ██╗███╗   ██╗███████╗██████╗ 
██╔══██╗██║ ██╔╝██║    ██║████╗  ██║██╔════╝██╔══██╗
██████╔╝█████╔╝ ██║ █╗ ██║██╔██╗ ██║█████╗  ██████╔╝
██╔═══╝ ██╔═██╗ ██║███╗██║██║╚██╗██║██╔══╝  ██╔══██╗
██║     ██║  ██╗╚███╔███╔╝██║ ╚████║███████╗██║  ██║
╚═╝     ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
``` 
A Python3 PoC for CVE-2021-4034 by Kim Schulz

# Intro

This is a simple Python3 PoC for the newly found Polkit error names [PwnKit](https://blog.qualys.com/vulnerabilities-threat-research/2022/01/25/pwnkit-local-privilege-escalation-vulnerability-discovered-in-polkits-pkexec-cve-2021-4034).

The issue is very simple to abuse but has huge consequences as it will easily give root access on most linux machines where the attacker has local user access. 

# How to run
This script is a one shot execution so simply do
```
python3 pkwner.py
```
It should look something like this:
![alt text](https://github.com/kimusan/pkwner/raw/main/screenshot.png "screenshot")
