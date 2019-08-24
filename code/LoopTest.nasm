 Filename: LoopTest.nasm
; Author: Michael Norris

global _start

section .text
_start:

SetCounter:
    mov ecx, 0x5 
    
SaveCounter:
    push ecx 

PrintMessage:
    mov eax, 0x4        ; sys_write
    mov ebx, 0x1    
    mov ecx, message
    mov edx, mlen
    int 0x80

LoopDemo:
    pop ecx 
    loop SaveCounter    ; decrements counter (ECX) and jumps to label

Exit:
    mov eax, 0x1        ; sys_exit
    mov ebx, 0x0 
    int 0x80

section .data
    message: db "Loop",0xa
    mlen: equ $ - message
