all: remoteServer remoteClient

remoteServer: remoteServer.c
	gcc -o remoteServer remoteServer.c

remoteClient: remoteClient.c
	gcc -o remoteClient remoteClient.c

clean:
	rm -f remoteServer remoteClient *.o
