/***************************************
****************************************
** COMP211 @ TUC                      **
** Manesis Athanasios : 2014030061    **
** LAB21142503                        **
** Client-Server Project 3            **
****************************************
****************************************/

#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <arpa/inet.h>

// Function for reading File: DOESNT WORK 
/*
const char *readFile(FILE *file){

int maximumLineLength=128;

	if (file == NULL){ 
		printf("ERROR: fp is null.");
		exit(1);	
	}

char *lineBuffer = (char *)malloc(sizeof(char) * maximumLineLength);

	if (lineBuffer == NULL){
		printf("ERROR: memory allocation");      
	}

char ch = getc(file);
int count = 0;

	while ((ch!='\n') && (ch!=EOF)){
		if (count == maximumLineLength){
			maximumLineLength+=128;
			lineBuffer=realloc(lineBuffer, maximumLineLength);
				if (lineBuffer==NULL)
				{ exit(1) }	
		}	
		lineBuffer[count]=ch;
		count++;
		ch=getc(file);
	}S

	 lineBuffer[count] = '\0';
    	char line[count + 1];
    	strncpy(line, lineBuffer, (count + 1));
    	free(lineBuffer);
    	const char *constLine = line;
    	return constLine;

}
*/

int main(int argc, char *argv[]){
  char msg[10000];
  int server, portno;
  struct sockaddr_in servAdd;     // structure contains socket address and is defined in <netinet/in.h>
  
 if(argc != 5){
    printf("Call Syntax: %s <serverName> <serverPort> <receivePort> <inputFileWithCommands>\n", argv[0]);
    exit(0);
  }
  
  // Socket Creation Syntax socket(domain, type, protocol);
  if ((server = socket(AF_INET, SOCK_STREAM, 0)) < 0){
     fprintf(stderr, "Socket cannot be created\n");
     exit(1);
  }

  servAdd.sin_family = AF_INET;
  sscanf(argv[2], "%d", &portno);           
  servAdd.sin_port = htons((uint16_t)portno); // host to network byte conversion
  
  // inet_pton - Convert IP addresses from text to binary form 
  if(inet_pton(AF_INET, argv[1], &servAdd.sin_addr) < 0){ // returns 0 if argv[1] does not have a valid address; returns -1 if af has invalid address family
  fprintf(stderr, " inet_pton() Failed\n");
  exit(2);
}
// Connection on socket  
 if(connect(server, (struct sockaddr *) &servAdd, sizeof(servAdd))<0){ // returns -1 on failure; returns 0 on success
  fprintf(stderr, "connect() Failed\n");
  exit(3);
 }

/* PROBLEM WITH READING
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

  readFile(argv[4]); 

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
*/
 
 while(1){ // Client enters infinite loop
 
  fprintf(stderr, "If you want to leave, enter quit or else enter the bash command to be executed\n");
  fgets(msg, 10000, stdin); // reads client command from Standard Input i.e. Keyboard
  
//Write client commands to the server
  write(server, msg, strlen(msg)+1); // with length of 0 appended to the string by default
  
   if(strcmp("quit\n",msg)==0) 
   {
	    close(server);       // close server if quit is entered by client
    exit(0);
   }
  
  // read the output of command from server to the client
  char c;
  char str1[1024];
  int i=0;
  while(1) // Infinite loop
  {	
  if (!read(server, &c, 1)){
	   close(server);
    fprintf(stderr, "read() Error\n");
    exit(0); 
 }
		str1[i]=c;
		i++;
		if(c=='\n')
		{
			str1[i-1]='\0';
			i=0;
		}
   fprintf(stderr, "%c", c);
   if(strcmp("[ DONE ]",str1)==0) 
   {
	    fprintf(stderr, "\n"); 
	   break;     // Breaks this if and continues loop if receives DONE from server
   }
  }
}
}


