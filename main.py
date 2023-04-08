from http.server import HTTPServer, BaseHTTPRequestHandler
from config import bot,asisstant
from pyrogram import filters,idle
from threading import Thread





class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            with open('templates/index.html', 'r') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(content, 'utf8'))
        except:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404: File not found')

def http_run():
  httpd = HTTPServer(('', 8000), MyHandler)
  httpd.serve_forever()

def run_thread():
  Thread(target=http_run).start()

def run():
  run_thread()
  bot.start()
  asisstant.start()
  print("START BOT")
  idle()
  bot.stop()
  asisstant.stop()

run()
