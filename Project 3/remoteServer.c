/***************************************
****************************************
** COMP211 @ TUC                      **
** Manesis Athanasios : 2014030061    **
** LAB21142503                        **
** Client-Server Project	      **
****************************************
****************************************/

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>

void child(int); // function declaration

void exeCommand(char* str) 
{ 
while(1)
{
int n;
char ch;
    int count=0;
	int cmdCount=0;
	char command[200][100];
	char idn[200];
	int i=0;
	char indentifier=';';
    while(count <= strlen(str)) 
    {		
		if(str[count]==';'|| str[count]=='&' || str[count]=='|')
		{	
			if(str[count]=='&')
			{
				indentifier='&';
			}
			else if(str[count]=='|')
			{
				indentifier='|';
			}
			else{
				indentifier=';';
			}
			if(str[count]=='&' && str[count+1]=='&' )
			{
				
			}
			else if(str[count]=='|' && str[count+1]=='|' )
			{
				
			}
			else{
				command[cmdCount][i]='\0';
				idn[cmdCount]=indentifier;			
			    cmdCount++;
			 i=0;
			}
		}
		else{
			command[cmdCount][i]=str[count];
			i++;
			
		}
		count++;      
    }
	idn[cmdCount]=';';

for(i=0;i<=cmdCount;i++)
{
      printf("\nCommand: %s\n", command[i]);
      char *args[10] = {}; 
      args[0] = strtok(command[i], " "); // get the first token using string tokenizer
      int tokencount = 0;
	  
      // Walk through other tokens
      while (args[tokencount] != NULL){
        tokencount++;
        args[tokencount] = strtok(NULL, " ");
      }

      int childpid = fork(); //Perform fork()

  if (childpid == 0) // Child Process
    { 
         if ((execvp(args[0], args)) < 0)// returns -1 if execvp is unsuccessful; 
         { 
           printf("Error! Command can not be found\n\n");
           exit(-1);
         }
         exit(0);
    }
	  else if (childpid > 0) // Parent Process
	  {  	  
        int status;       
        wait(&status);              // Waits for the exit status of child
              if(WIFEXITED(status))
		      {
                int exitstatus = WEXITSTATUS(status);
		          if(exitstatus ==0)
		          {
		              if(idn[i]=='|')
		        	    {
		        		    i=cmdCount+1;
		        	    }
		          }		  
		          else
		          {
		        	     printf("Error with command");
		        	     if(idn[i]=='&')
		        	     {
		        		  i=cmdCount+1;
					
		        	     }
		          }
              }
		      else
		     {
			  printf("Signaled Status =%d\n",WTERMSIG(status));
		     }
      }
 else{
      printf("Error\n");
      exit(1);
    }
 } 
  break;
 }	
}

//Main function
int main(int argc, char *argv[]){  
  int sd, client, portno;
  struct sockaddr_in servAdd;     // structure contains socket address and is defined in <netinet/in.h>
  
 if(argc != 3){
    printf("Call Syntax: %s <portNumber> <numChildren> \n", argv[0]);
    exit(0);
  }

  sd = socket(AF_INET, SOCK_STREAM, 0); //socket descriptor
  servAdd.sin_family = AF_INET;
  servAdd.sin_addr.s_addr = htonl(INADDR_ANY); // INADDR_ANY - Server's IP address will be automatically assigned
  sscanf(argv[1], "%d", &portno);
  servAdd.sin_port = htons((uint16_t)portno); // host to network short byte conversion
  
  // bind() function binds a socket to the address of the current host and port number on which the server will run
  bind(sd, (struct sockaddr *) &servAdd, sizeof(servAdd));
  listen(sd, 5); //5 Is the maximum size backlog queue, i.e., the number of connections that can be waiting while the process is handling a particular connection. 

  while(1){ // Infinite Loop
  
  // accept() blocks the process until client gets connected to the server
      client = accept(sd, NULL, NULL);
	
    printf("Got a client\n");

    if(!fork()) // Child Process 
      child(client); // Child process calls child() to perform the command

    close(client); // Parent Process get backs and waits for other client
   }
}


void child(int sd){
	
	char msg[2000];
	
  while(1){ // Infinite Loop
		fprintf(stderr, "Waiting for command\n");
		
		//reads command from client
		if(!read(sd, msg, 255)){
			close(sd);
			fprintf(stderr, "Client exit\n");
			exit(0);
		  }
		  
		// print client command
		fprintf(stderr, "Client's command: (%s)\n", msg); 
		
		dup2(sd,1); // Now, writing to standard output means writing to socket descriptor sd
		
		//Execute client command
		 printf("Running command\n");
		 int len=strlen(msg);
		 msg[len-1]='\0';
		 fprintf(stderr, "Running command: (%s)\n", msg);
		 exeCommand(msg); // call exeCommand() 
		 printf("\n");
		 printf("[ DONE ]\n");
		
	   }
}
