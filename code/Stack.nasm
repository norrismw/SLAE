; Stack.nasm 
; Author: Michael Norris
; Purpose: Demonstration of storing a string on the stack

global _start

section .text
_start:

shellcode:
    ; "Hello, world!\n" 
    xor edx, edx 
    push edx                ; Null characters to terminate string. PUSHed first, read last
    xor ecx, ecx    
    mov cx, 0x0a21          ; '!\n' If not divisible by 4, pass the remainder characters first
    push cx                 ; Since byte count of string isn't divisible by 4, pass string through low register
    push 0x646c726f         ; 'orld!\n' 
    push 0x77202c6f         ; 'o, world!\n'
    push 0x6c6c6548         ; 'Hello, world!\n'

    ; 'sys_write'
    xor eax, eax 
    mov al, 0x4 
    xor ebx, ebx 
    mov bl, 0x1 
    xor ecx, ecx 
    mov ecx, esp            ; ESP points to 'Hello, world!\n' and reads until it reaches 0x00
    mov dl, 14              ; 'Hello, world!\n' is 14 bytes
    int 0x80

    ; sys_exit
    xor eax, eax 
    mov al, 0x1 
    xor ebx, ebx 
    int 0x80

