#!/usr/bin/env python3
import socket
import os
import sys
import signal

def READ(dict):

def LS(dict):

def LENGTH(dict):

def SPLITHEADER(line):
	line = line.strip() # odstranenie medzier (na konci/ na zaciatku)
	line=line.split(':') #rozdelenie na identifikator a hodnotu
	if(len(line) != 2):
		return '', '' 

	#kontrola identifikatora
	if not isascii(line[0]): #kontroler ascii znakov 
		return '', ''

	for char in line[0]:   
		if(char.isspace()): #kontrola bielych znakov
			return '', ''

	if(line[0].find(':') != -1): # nesmie obsahovat dvojbodku
		return '', ''


	if(line[0].find('/') != -1): # nesmie obsahovat lomitko
		return '', ''

	return line[0], line[1]

######################################################################	

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 9999))
signal.signal(signal.SIGCHLD, signal.SIG_IGN)
s.listen(5)

while True:
    connectedSocket, address = s.accept()
    print(f'connection from adress: {address}')
    pid_chld = os.fork()
    if pid_chld == 0:
        s.close()
        f = connectedSocket.makefile(mode='rw', encoding='utf-8')

        while True:

            method = f.readline().strip() #precitanie metody
            if not method: # ak sa neprecita ziadna metoda tak break
                break

            data = f.readline()

            while data != "\n":
              identifier, value = SPLITHEADER(data) # rozdelenie hlavicky
              headers[identifier]= value #ulozenie hlavicky 
              data = f.readline() #precitanie dalsieho riadku 

            statusCode, statusMsg = (100, 'OK')

            if method == 'READ':
            	headerReply, contentReply, statusCode, statusMsg = READ(headers)

            elif method == 'LS':
                headerReply, contentReply, statusCode, statusMsg = LS(headers)

            elif method == 'LENGTH':
                headerReply, contentReply, statusCode, statusMsg = LENGTH(headers)

            else:
                statusCode, statusMsg = (204, 'Unknown method')

                f.write(f'{statusCode} {statusMsg}\n')
                f.write('\n')
                f.flush()
                sys.exit(0)

            f.write(f'{statusCode} {statusMsg}\n')
            f.write(headerReply)
            f.write('\n')
            f.write(contentReply)
            f.flush()
        print(f'{address} disconnected')
        sys.exit(0)
    else:
        connectedSocket.close()