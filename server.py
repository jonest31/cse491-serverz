#!/usr/bin/env python
import random
import socket
import time
import urlparse

#global variables
header = 'HTTP/1.0 200 OK\r\n' + \
                    'Content-type: text/html\r\n' + \
                    '\r\n'

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
    request = conn.recv(1000)
    print request

    first_line = request.split('\r\n')[0].split(' ')

    # Path is the second element in the first line of the request
    # separated by whitespace. (Between GET and HTTP/1.1). GET/POST is first.
    http_method = first_line[0]
            
    try:
        parsed_url = urlparse.urlparse(first_line[1])
        path = parsed_url[2]
    except:
        path = "/404"

        
    # send a response
    if http_method == 'POST':
        if path == '/':
            handle_index(conn, '')
        elif path == '/submit':
            # POST has the submitted params at the end of the content body
            handle_submit(conn,request.split('\r\n')[-1])
    else:
        if path == '/':
            handle_index(conn,'')
        elif path == '/content':
            handle_content(conn,'')
        elif path == '/file':
            handle_file(conn,'')
        elif path == '/image':
            handle_image(conn,'')
        elif path == '/submit':
            handle_submit(conn,parsed_url[4])  #!!!!!!!!!!
        else:
          notfound(conn,'')
        conn.close()

def handle_index(conn, params):
  #Handle a connection given path / 
  conn.send('HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n' + \
            '\r\n' + \
            "<p><u>Form Submission via GET</u></p>"
            "<form action='/submit' method='GET'>\n" + \
            "<p>first name: <input type='text' name='firstname'></p>\n" + \
            "<p>last name: <input type='text' name='lastname'></p>\n" + \
            "<p><input type='submit' value='Submit'>\n\n" + \
            "</form></p>" + \
            "<p><u>Form Submission via POST</u></p>"
            "<form action='/submit' method='POST'>\n" + \
            "<p>first name: <input type='text' name='firstname'></p>\n" + \
            "<p>last name: <input type='text' name='lastname'></p>\n" + \
            "<p><input type='submit' value='Submit'>\n\n" + \
            "</form></p>")
      
def handle_submit(conn, params):
    #Handle a connection given path /submit
    # submit needs to know about the query field, so more
    # work needs to be done here
    
    params = urlparse.parse_qs(params)

    # format is name=value. We want the value.
    firstname = params['firstname'][0]

    lastname = params['lastname'][0]

    #print firstname
    #print lastname
    #print params

    conn.send(header + \
              "Hello Ms. %s %s." % (firstname, lastname))
    
def handle_content(conn, params):
    #Handle a connection given path /content
    conn.send(header + \
            '<h1>MSU SMB ftw</h1>' + \
            'some content')

def handle_file(conn, params):
    #Handle a connection given path /file
    conn.send(header + \
            '<h1>On the banks of the read cedar</h1>' + \
            'some file')

def handle_image(conn, params):
    #Handle a connection given path /image
    conn.send(header + \
            '<h1>Theres a school thats known to all</h1>' + \
            'some image')

def notfound(conn, params):
    conn.send(header + \
            "404 Not Found" + \
            '<h1>rut roh you did it wrong...</h1>')

if __name__ == '__main__':
   main()


