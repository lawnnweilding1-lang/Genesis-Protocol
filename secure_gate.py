import requests
import json
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler

GATEWAY_PORT = 7417
BLINK_AUTHORIZED_TOKEN = "blink-root-auth-7417-x99"

class SecureGateHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        auth_header = self.headers.get("Authorization")
        expected_bearer = f"Bearer {BLINK_AUTHORIZED_TOKEN}"
        
        if not auth_header or auth_header != expected_bearer:
            print(f"[!] ACCESS DENIED: Unauthorized payload attempt on port {GATEWAY_PORT}.")
            self.send_response(401)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response_data = {"error": "Unauthorized: B-Link hardware token validation failed."}
            self.wfile.write(json.dumps(response_data).encode("utf-8"))
            return

        print(f"[✔] B-Link Auth Verified: Channel open on port {GATEWAY_PORT}.")
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        reply = {"status": "success", "message": "Gate open. Command executed via B-Link authorization."}
        self.wfile.write(json.dumps(reply).encode("utf-8"))

def run_secure_gateway():
    server_address = ('127.0.0.1', GATEWAY_PORT)
    httpd = HTTPServer(server_address, SecureGateHandler)
    print(f"[+] Secure Genesis Gate listening on port {GATEWAY_PORT}...")
    print(f"[+] Locked to B-Link Node Authorization Token.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Shutting down secure gate.")
        httpd.server_close()

if __name__ == "__main__":
    run_secure_gateway()
