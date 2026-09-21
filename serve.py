#!/usr/bin/env python3
import http.server
import socketserver
import subprocess
import threading
import time
import re
import os

PORT = 8999
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def start_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Local server running on port {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    # Ensure index.html exists
    idx = os.path.join(DIRECTORY, "index.html")
    cal = os.path.join(DIRECTORY, "sports_calendar.html")
    if not os.path.exists(idx) and os.path.exists(cal):
        os.symlink("sports_calendar.html", idx)

    # Start local HTTP server in background thread
    t = threading.Thread(target=start_server, daemon=True)
    t.start()
    time.sleep(1)

    # Launch cloudflared quick tunnel
    cmd = ["/tmp/cloudflared", "tunnel", "--url", f"http://localhost:{PORT}"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    tunnel_url = None
    for line in iter(proc.stdout.readline, ''):
        print(line, end='', flush=True)
        m = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
        if m and not tunnel_url:
            tunnel_url = m.group(0)
            url_file = os.path.join(DIRECTORY, "public_url.txt")
            with open(url_file, "w") as f:
                f.write(tunnel_url + "\n")
            print(f"\n============================================\nPUBLIC URL READY: {tunnel_url}\n============================================\n", flush=True)
            print("🟢 Server & Cloudflare Tunnel are actively running in the foreground.", flush=True)
            print("   (This process intentionally stays open to keep your site online. Press Ctrl+C to stop.)\n", flush=True)

    proc.wait()
