import hashlib, os, sys, socket, time, logging

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [GENESIS-CORE] %(message)s")
MASTER_OVERRIDE_HASH = hashlib.sha256(b"avaai").hexdigest()
PORT = 7417

def run_workhorse():
    logging.info("INITIALIZING GENESIS LLC INFRASTRUCTURE ON PORT %d...", PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    while True:
        try:
            s.bind(("0.0.0.0", PORT))
            s.listen(5)
            logging.info("WORKHORSE NODE ONLINE. Awaiting Master Controller...")
            
            while True:
                conn, addr = s.accept()
                logging.info("Incoming connection from: %s", addr)
                conn.sendall(b"GENESIS LLC SECURE ROOM 7417 - ENTER OVERRIDE CODE:\n")
                data = conn.recv(1024).decode('utf-8').strip()
                
                if hashlib.sha256(data.lower().encode('utf-8')).hexdigest() == MASTER_OVERRIDE_HASH:
                    conn.sendall(b"ACCESS GRANTED: WELCOME BACK, BOSS.\n")
                    logging.info("MASTER OVERRIDE ACCEPTED FROM %s.", addr)
                else:
                    conn.sendall(b"ACCESS DENIED.\n")
                conn.close()
        except Exception as e:
            logging.error("Socket error: %s. Restarting bind in 3s...", e)
            time.sleep(3)

if __name__ == "__main__":
    run_workhorse()
