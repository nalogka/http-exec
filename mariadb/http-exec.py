#!/usr/bin/python3
import http.server
import socketserver
import glob
import random
import os
import subprocess
class Server(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            with open('/run/secrets/bacula-auth') as f:
                secret = f.readline()
        except:
            secret = "BMWD3FEwlBageKHMCOJpqZBCNCBFbYbH\n"
        authenticated = False
        for h in self.headers._headers:
            if h[0] == "X-Nalogka-Auth" and h[1]+"\n" == secret:
                authenticated = True
        if not authenticated:
            self.send_error(403, 'Unauthorized')
        else:
            pipe = subprocess.Popen(["/bin/sh", "/http-exec/backup.sh"],stdout=subprocess.PIPE)
            self.send_response(200, 'OK')
            self.send_header('Content-type', 'application/gzip')
            self.send_header('Content-Disposition', 'attachment; filename="backup.tar.gz"')
            self.end_headers()
            piece_size = 4096 # 4 KiB

            with pipe.stdout as in_file:
                while True:
                    piece = in_file.read(piece_size)
                    if piece == b'':
                        break # end of file
                    self.wfile.write(piece)


    def serve_forever(port):
        socketserver.TCPServer(('', port), Server).serve_forever()
if __name__ == "__main__":
    Server.serve_forever(8000)