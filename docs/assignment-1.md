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
Next, the `addr` IP socket address structure is created which is used in the forthcoming `bind` method. As further explained in `man 7 ip`, an IP socket address is defined as a combination of an IP interface address and a 16-bit (2 byte) port number. The man page also states that `sin_family` is always set to `AF_INET`, that `sin_port` defines a port number in network byte order, and that `sin_addr` is the host IP address and should be assigned one of the `INADDR_*` values. 

In the code above, the `htons` function converts the unsigned short integer `4444` from host byte order to network byte which is the format expected for `sin_port`. The value of `INADDR_ANY` (which correlates to `0.0.0.0` or "any") is given for `sin_addr`.

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

## Wrapper Program for Port Configuration

_This blog post has been created for completing the requirements of the SecurityTube Linux Assembly Expert certification:_

<http://securitytube-training.com/online-courses/securitytube-linux-assembly-expert>

_Student ID: SLAE-1469_
---
[Home](https://norrismw.github.io/SLAE)
