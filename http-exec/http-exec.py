#!/usr/bin/python3
import http.server
import socketserver
import glob
import random
import os
import subprocess
class Server(http.server.SimpleHTTPRequestHandler):
    def do_GET(self): 
        # Проверка аутентификации
        if os.environ.get('HTTP_EXEC_USE_AUTHENTICATION') is None or os.environ['HTTP_EXEC_USE_AUTHENTICATION'].lower == "true" or os.environ['HTTP_EXEC_USE_AUTHENTICATION'].lower == "yes":
            try:
                with open(os.environ['HTTP_EXEC_SECRET_PATH']) as f:
                    secret = f.readline()
                    if secret.endswith('\n'):
                        secret = secret[:-1]
                    f.close()
            except:
                secret = ""
            authenticated = False
            if secret != "":
                for h in self.headers._headers:
                    if h[0] == "X-Nalogka-Auth" and h[1] == secret:
                        authenticated = True
            if not authenticated:
                self.send_error(403, 'Unauthorized')
                return 0
        execpath = os.environ['HTTP_EXEC_BINARY_FOLDER_PATH']
        if execpath.endswith('/'):
            execpath = execpath[:-1]
        if self.path.count('/') > 1:
            self.send_error(404, 'Not found')
        elif os.path.isfile(execpath+self.path) and os.access(execpath+self.path, os.X_OK):
            pipe = subprocess.Popen([execpath+self.path],stdout=subprocess.PIPE,shell=True)
            self.send_response(200, 'OK')
            self.send_header('Content-type', 'application/octet-stream')
            self.end_headers()
            piece_size = 4096 # 4 KiB
            with pipe.stdout as in_file:
                while True:
                    piece = in_file.read(piece_size)
                    if piece == b'':
                        break # end of file
                    self.wfile.write(piece)
        else:
            self.send_error(404, 'Not found')


    def serve_forever(port):
        socketserver.TCPServer(('', port), Server).serve_forever()
if __name__ == "__main__":
    Server.serve_forever(8000)