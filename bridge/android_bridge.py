"""
Saathi AI — Android Cross-Device Companion Bridge
Local TCP Socket listener on port 8890 for Android notification sync, SMS/call alerts,
and bidirectional clipboard synchronization.
"""

import json
import socket
import threading
import time
from typing import Dict, Any, Callable, Optional, List

class AndroidBridgeServer:
    """
    Local Wi-Fi & USB ADB Companion Bridge for Android synchronization.
    """
    def __init__(self, host: str = "0.0.0.0", port: int = 8890):
        self.host = host
        self.port = port
        self.running = False
        self.server_socket: Optional[socket.socket] = None
        self.thread: Optional[threading.Thread] = None
        self.handlers: Dict[str, List[Callable[[Dict[str, Any]], None]]] = {}
        self.last_phone_clipboard: str = ""
        self.connected_device: Optional[str] = None

    def register_handler(self, event_type: str, callback: Callable[[Dict[str, Any]], None]):
        """Register callback for specific Android event (e.g. 'call_alert', 'sms', 'clipboard')."""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(callback)

    def start(self):
        """Start local companion socket listener thread."""
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._server_loop, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop local companion socket listener."""
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except Exception:
                pass

    def _server_loop(self):
        """Bind socket and process incoming companion connections."""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.server_socket.settimeout(2.0)

            while self.running:
                try:
                    conn, addr = self.server_socket.accept()
                    self.connected_device = addr[0]
                    threading.Thread(target=self._handle_client, args=(conn,), daemon=True).start()
                except socket.timeout:
                    continue
                except Exception:
                    time.sleep(0.5)

        except Exception:
            pass
        finally:
            if self.server_socket:
                try:
                    self.server_socket.close()
                except Exception:
                    pass

    def _handle_client(self, conn: socket.socket):
        """Handle incoming JSON payload from Android device."""
        try:
            conn.settimeout(5.0)
            data = conn.recv(8192)
            if not data:
                conn.close()
                return

            payload = json.loads(data.decode('utf-8'))
            event_type = payload.get("event", "unknown")

            if event_type == "clipboard":
                self.last_phone_clipboard = payload.get("text", "")

            # Dispatch to handlers
            if event_type in self.handlers:
                for cb in self.handlers[event_type]:
                    try:
                        cb(payload)
                    except Exception:
                        pass

            # Acknowledge response
            response = json.dumps({"status": "received", "event": event_type, "timestamp": time.time()})
            conn.sendall(response.encode('utf-8'))
        except Exception:
            pass
        finally:
            try:
                conn.close()
            except Exception:
                pass

