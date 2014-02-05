import server

class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r
            
        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def close(self):
        self.is_closed = True

# Test a basic GET call.
def test_handle_connection():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      "<p><u>Form Submission via GET</u></p>" + \
                      "<form action='/submit' method='GET'>\n" + \
                      "<p>first name: <input type='text' name='firstname'></p>\n" + \
                      "<p>last name: <input type='text' name='lastname'></p>\n" + \
                      "<p><input type='submit' value='Submit'>\n\n" + \
                      "</form></p>" + \
                      "<p><u>Form Submission via POST</u></p>" +\
                      "<form action='/submit' method='POST'>\n" + \
                      "<p>first name: <input type='text' name='firstname'></p>\n" + \
                      "<p>last name: <input type='text' name='lastname'></p>\n" + \
                      "<p><input type='submit' value='Submit'>\n\n" + \
                      "</form></p>"

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

#test content call
def test_handle_content_connection():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>MSU SMB ftw</h1>some content'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

#test file call
def test_handle_file_connection():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>On the banks of the read cedar</h1>some file'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

#test image call
def test_handle_image_connection():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Theres a school thats known to all</h1>some image'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

#test post call
def test_handle_post_connection():
    conn = FakeConnection("POST / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
		      "<p><u>Form Submission via GET</u></p>" +\
                      "<form action='/submit' method='GET'>\n" + \
                      "<p>first name: <input type='text' name='firstname'></p>\n" + \
                      "<p>last name: <input type='text' name='lastname'></p>\n" + \
                      "<input type='submit' value='Submit'>\n\n" + \
                      "</form></p>" + \
                      "<p><u>Form Submission via POST</u></p>" +\
                      "<form action='/submit' method='POST'>\n" + \
                      "<p>first name: <input type='text' name='firstname'></p>\n" + \
                      "<p>last name: <input type='text' name='lastname'></p>\n" + \
                      "<p><input type='submit' value='Submit'>\n\n" + \
                      "</form></p>"

    server.handle_connection(conn)
    print expected_return
    print repr(expected_return)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

    
#test submit call
def test_handle_submit():
    conn = FakeConnection("GET /submit?firstname=Tay&lastname=Jones " + \
                          "HTTP/1.1\r\n\r\n")

    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      "Hello Ms. Tay Jones."

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

# Test /submit requests
def test_handle_submit_post():
    conn = FakeConnection("POST /submit " + \
                          "HTTP/1.1\r\n\r\nfirstname=Tay&lastname=Jones")

    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      "Hello Ms. Tay Jones."

    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)






