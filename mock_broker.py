from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class BrokerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response_data = {
            "status": "success",
            "address": "14T259V4v133j2x45e2K4s3R6T5h7y2w8",
            "balance": "0.00",
            "state": "verified_air_gapped"
        }
        self.wfile.write(json.dumps(response_data).encode())
    def log_message(self, format, *args):
        return

print("[*] Starting local mock mesh broker on port 7417...")
server = HTTPServer(('127.0.0.1', 7417), BrokerHandler)
server.serve_forever()
