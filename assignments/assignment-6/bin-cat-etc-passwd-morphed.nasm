global _start

section .text
_start:
    xor eax, eax 
    mul eax                     ; change #1
    push edx 
    push dword 0x7461632f
    push dword 0x6e69622f
    mov ebx, esp 
    push edx 
    jmp short jump_a            ; change #2

call_a:
    pop ecx                     ; change #3
    mov al, 0xb 
    push edx 
    push ecx 
    push ebx 
    mov ecx, esp 
    int 0x80

jump_a:
    call call_a
    db '/etc/passwd'
