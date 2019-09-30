## Assignment 0x01: Create A Shell_Bind_TCP Shellcode
---
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

    // Designate Socket to Accept Connection Requests
    listen(sockfd, 0);

    // Accept Connection Requests
    int connfd = accept(sockfd, NULL, NULL);

    // Direct Output
    for (int i = 0; i < 3; i++)
    {
        dup2(connfd, i);
    }

    execve("/bin/sh", NULL, NULL);
    return 0;
}
```

## Analysis of Shell_Bind_TCP.c
#### Create a TCP Socket with socket()
`int socket(int domain, int type, int protocol);`

First, a TCP socket is created using the `socket` function. As described in `man 2 socket`, the function creates an endpoint for communication and returns a file descriptor that refers to that endpoint. `socket()` expects a domain argument, a type argument, and a protocol argument.

In this case, the domain argument `AF_INET` specifies the IPv4 communication protocol, the type argument `SOCK_STREAM` specifies the connection-based TCP standard for data exchange, and the protocol argument `0` indicates that the system should select the default protocol number based on the previously specified domain and protocol arguments.

#### Create an IP Socket Address Structure
Next, the `addr` IP socket address structure is created which is used in the forthcoming `bind` method. As further explained in `man 7 ip`, an IP socket address is defined as a combination of an IP interface address and a 16-bit (2 byte) port number. The man page also states that `sin_family` is always set to `AF_INET`, that `sin_port` defines a port number in network byte order, and that `sin_addr` is the host IP address and should be assigned one of the `INADDR_*` values. 

In the code above, the `htons` function converts the unsigned short integer `4444` from host byte order to network byte order as expected by `sin_port`. The value of `INADDR_ANY` (which correlates to `0.0.0.0` or "any") is given for `sin_addr`.

#### Bind TCP Socket to IP Socket Address Structure with bind()
`int bind(int sockfd, const struct sockaddr *addr, socklen_t addrlen);`

The `bind` method is now used to bind the TCP socket as created by `socket()` to the port and IP address initialized within the `addr` structure. From `man bind`, the `bind()` system call takes three arguments; a socket file descriptor (`sockfd`), a pointer to a structure of the type `sockaddr_in` (`addr`), and the size, in bytes (returned by the `sizeof` operator in this example), of the address structure pointed to by the second argument.

#### Designate Socket to Accept Connection Requests with listen()
`int listen(int sockfd, int backlog);`

As the socket is now bound to an IP address and a port, the `listen` function is used to designate the socket as one which will be used to accept incoming connection requests through the `accept` function. As described in, `man 2 listen` the function expects two arguments. The first argument is a socket file descriptor (once again, the socket defined as `sockfd`), and the second argument identifies how many pending connections should be queued.

#### Accept Connection Requests with accept()
`int accept(int sockfd, struct sockaddr *addr, socklen_t *addrlen);`

#### Direct Output with dup2()
`int dup2(int oldfd, int newfd);`

#### Execute Program with execve()
`int execve(const char *pathname, char *const argv[], char *const envp[]);`

## From C to Shellcode

## Wrapper Program for Port Configuration

_This blog post has been created for completing the requirements of the SecurityTube Linux Assembly Expert certification:_

<http://securitytube-training.com/online-courses/securitytube-linux-assembly-expert>

_Student ID: SLAE-1469_

---
[Home](https://norrismw.github.io/SLAE)
