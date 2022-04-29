#!/usr/bin/env python3
import socket
import os
import sys
import signal

def READ(dict):
	#kontrola hodnot from a to 
	

	try:
		with open(f'data/{dict["File"]}', 'r') as file:
			fileContent = file.readlines()
			lines = len(flieContent) #pocet riadkov v subore
			
			if(not isinstance(dict["From"],int)) or (dict["From"] < 0 ):
				return '','',200,'Bad request'

			if(not isinstance(dict["To"],int)) or (dict["To"] < 0 ) or (dict["To"] < dict["From"]):  
				return '','',200,'Bad request'
			
			if(dict["To"] > (lines - 1)):
				return '','',201,'Bad line number'

    except FileNotFoundError:
        return '','',202,'No such file'
    except OSError:
        return '','',203,'Read error'
    except KeyError:
        return '','',200,'Bad request'

    headerReply = f'Lines:{dict["To"] - dict["From"]}' # hlavicka odpovede
    contentReply = [lines[i] for i in range(dict["From"], dict["To"])] # vybranie konkretnych riadkov zo suboru
    contentReply = ''.join(contentReply) # spojenie riadkov do jedneho stringu 

    return headerReply, contentReply, 100, 'OK'


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
qhp_Qg89vY6qQtrbMkt16Eh0H4PE5nuPyy098o6D
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