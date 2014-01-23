#!/usr/bin/env python
import random
import socket
import time

def main():
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn() # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(c)
        
        
def handle_connection(conn):

    #get the request message
    request = conn.recv(1000).split('\n')[0]
    method = request.split(' ')[0]
    path = request.split(' ')[1]
    
    # send a response
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n\r\n')
    response_body = ' '
    if method == 'POST':
        response_body = '<h1>Post</h1>Blah'
    elif path == '/':
	response_body = '<h1>Links to other pages</h1>' + \
                      '<a href = /content>Content</a><br>' + \
                      '<a href = /file>File</a><br>' + \
                      '<a href = /image>Image</a>'
    elif path == '/content':
	response_body = '<h1>Are we there yet</h1>Please'
    elif path == '/file':
	response_body = '<h1>On the banks of the read cedar</h1>winning'
    elif path == '/image':
	response_body = '<h1>There is light at the end of this tunnel</h1>SO CLOSE'

    #conn.send('<h1>Hello, world.</h1>')
    #conn.send('This is jonest31\'s Web server.')
    conn.send(response_body)
    conn.close()

if __name__ == '__main__':
   main()


