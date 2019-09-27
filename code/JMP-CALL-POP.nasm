; JUMP-CALL-POP.nasm 
; Author: Michael Norris
; Purpose: Demonstration of JUMP-CALL-POP

global _start

section .text
_start:
; 1: JUMP -- JUMPs to 'call_shellcode' label
    jmp short call_shellcode

; 3: POP -- POPs location of 'message' from the stack to ECX as part of setting registers for 'sys_write'
shellcode:
    ; sys_write
    xor eax, eax 
    mov al, 0x4 
    xor ebx, ebx 
    mov bl, 0x1 
    pop ecx 
    xor edx, edx 
    mov dl, 14
    int 0x80
; sys_exit
    xor eax, eax 
    mov al, 0x1 
    xor ebx, ebx 
    int 0x80

; 2: CALL -- PUSHes location of 'message' to stack due to the behavior of CALL & moves execution to 'shellcode' label
; Note: Placing this at the bottom of the code results in no 0x00 in 'objdump' due to higher memory location
call_shellcode:
    call shellcode
    message: db "Hello, world!", 0xA 
