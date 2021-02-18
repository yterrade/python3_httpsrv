#!/usr/bin/python3
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import sys
import base64
import ssl

key=''

class myHttp(SimpleHTTPRequestHandler):
    def do_POST(self):
        print('POST')
        self.send_response(200)
        self.end_headers();
        print (self.headers)
        print (self.rfile.read(int(self.headers['Content-Length'])))
        
    def do_PUT(self):
        print('PUT')
        self.send_response(200)
        self.end_headers();
        print (self.headers)
        print (self.rfile.read(int(self.headers['Content-Length'])))


class myHttpAuth(myHttp):
    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        global key
        if self.headers['Authorization'] == None:
            self.do_AUTHHEAD()
        elif self.headers['Authorization'] == 'Basic '+key:
        #base64.b64encode(bytes('Basic ','utf-8')) + key:
            myHttp.do_POST(self)
        else:
            self.do_AUTHHEAD()        

    def do_PUT(self):
        global key
        if self.headers['Authorization'] == None:
            self.do_AUTHHEAD()
        elif self.headers['Authorization'] == 'Basic '+key:
        #base64.b64encode(bytes('Basic ','utf-8')) + key:
            myHttp.do_PUT(self)
        else:
            self.do_AUTHHEAD()    

    def do_GET(self):
        global key
        if self.headers['Authorization'] == None:
            self.do_AUTHHEAD()
        elif self.headers['Authorization'] == 'Basic '+key:
        #base64.b64encode(bytes('Basic ','utf-8')) + key:
            SimpleHTTPRequestHandler.do_GET(self)
        else:
            self.do_AUTHHEAD()



if(len(sys.argv)>1):
    if(sys.argv[1] == '-s'):
        t = HTTPServer(('0.0.0.0',4443),myHttp)
        # generate cert with
        # openssl req -new -x509 -keyout mycert.pem -out mycert.pem -days 365 -nodes
        t.socket = ssl.wrap_socket(t.socket,server_side=True,certfile='mycert.pem')
    else:
        t = HTTPServer(('0.0.0.0',8000),myHttpAuth)
        key = base64.b64encode(bytes(sys.argv[1],'utf-8')).decode('utf-8')
else:
    t = HTTPServer(('0.0.0.0',8001),myHttp)
t.serve_forever()

## curl -d '{"k":"v"}' -H 'Content-type: application/json' -X POST http://toto:toto@127.0.0.1:8000
## curl -d '{"k":"v"}' -H 'Content-type: application/json' -X PUT http://toto:toto@127.0.0.1:8000


 
