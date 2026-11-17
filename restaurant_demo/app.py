"""Tiny restaurant-side API used to demonstrate the Compose integration."""

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen


class RestaurantHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status":"ok","restaurant":"demo-cafe"}')
            return
        if self.path == "/platform-status":
            with urlopen(os.environ["PLATFORM_URL"], timeout=2) as response:
                restaurants = json.load(response)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(restaurants).encode())
            return
        self.send_error(404)

    def log_message(self, format: str, *args: object) -> None:
        return


HTTPServer(("0.0.0.0", 8081), RestaurantHandler).serve_forever()
