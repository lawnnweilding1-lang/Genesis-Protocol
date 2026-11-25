import http.server
import socketserver
import json
import hashlib
import time

PORT = 7417

class GenesisHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        try:
            data = json.loads(body.decode('utf-8'))
        except Exception:
            data = {"raw": body.decode('utf-8', errors='ignore')}

        timestamp = time.time_ns()
        proof = hashlib.sha256(f"{timestamp}:{json.dumps(data, sort_keys=True)}".encode()).hexdigest()

        response = {
            "status": "COMMITTED_LOCAL",
            "node": "GENESIS-TERMUX-BRIDGE",
            "timestamp": timestamp,
            "state_proof": proof,
            "payload": data
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def log_message(self, format, *args):
        print(f"[GENESIS_LOG] {self.address_string()} - {format%args}")

with socketserver.TCPServer(("127.0.0.1", PORT), GenesisHandler) as httpd:
    print(f"[GENESIS CORE] Local bridge active on port {PORT}")
    httpd.serve_forever()
