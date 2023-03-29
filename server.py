import socket
import ssl
import random
import threading

context = ssl.create_default_context()
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('certs/cert.pem', 'certs/privkey.pem')

# Domain sample google.de
hostname = ""

def client_thread(sock):
    sock.send(("220 " + hostname + " ESMTP Postfix\n").encode())

    sock.recv(1024).decode()

    sock.send(("250-" + hostname + "\n250-PIPELINING\n250-SIZE 10240000\n250-VRFY\n250-ETRN\n250-STARTTLS\n250-ENHANCEDSTATUSCODES\n250-8BITMIME\n250-DSN\n250-SMTPUTF8\n250 CHUNKING\n").encode())

    print ("a")

    want = sock.recv(1024).decode()

    if "STARTTLS" in want:
        print ("b")
        sock.send(("220 2.0.0 Ready to start TLS\n").encode())
        print ("c")

        with context.wrap_socket(sock, server_side=True) as ssock:
            ssock.recv(1024).decode()

            ssock.send(("250-" + hostname + "\n250-PIPELINING\n250-SIZE 10240000\n250-VRFY\n250-ETRN\n250-ENHANCEDSTATUSCODES\n250-8BITMIME\n250-DSN\n250-SMTPUTF8\n250 CHUNKING\n").encode())
            
            mail_from = ssock.recv(1024).decode()
            mail_to = ""

            if "DATA" not in mail_from:
                ssock.send(("250 2.1.0 Ok\n").encode())
                mail_to = ssock.recv(1024).decode()

                ssock.send(("250 2.1.0 Ok\n").encode())

                ssock.recv(1024).decode()
            else:
                ssock.send(("250 2.1.0 Ok\n250 2.1.5 Ok\n").encode())


            ssock.send(("354 End data with <CR><LF>.<CR><LF>\n").encode())


            mail = ""
            
            while True:
                mail += ssock.recv(1024).decode()
                print(mail)

                #if len(mail) > 5:
                #    if "." in mail[-16:]:
                #        break

                if "QUIT" in mail[-16:]:
                    break


            
            ssock.send(("250 2.0.0 Ok: queued as " + ''.join((random.choice('0123456789ABCDEF') for i in range(10))) + "\n").encode())
            ssock.recv(1024).decode()
            ssock.send(("221 2.0.0 Bye\n").encode())

            # Todo DKIM signature verification

            ssock.close()
            




def server():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((hostname, 25))
    serversocket.listen(5)

    while True:
        (clientsocket, address) = serversocket.accept()
    
        #ct = client_thread(clientsocket)
        x = threading.Thread(target=client_thread, args=(clientsocket,))
        x.start()

server()