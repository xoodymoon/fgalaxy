import sys
import os
import http.server
import socketserver
import webbrowser
import threading
import time
from map_fwalker import scan_system
from exporter import generate_web_json

def build_bridge(tree_data):
    nodes = []
    edges = []

    def flatten(node, parent_idx=None):
        if not node: return
        current_idx = len(nodes)
        nodes.append({
            "name": node.get("name", "unknown"),
            "type": node.get("type", "file"),
            "family": node.get("family", "generic")
        })

        if parent_idx is not None:
            edges.append((parent_idx, current_idx))

        for child in node.get("children", []):
            flatten(child, current_idx)

    flatten(tree_data)
    return nodes, edges

def start_ui():
    install_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(install_dir)
    port = 8000
    handler = http.server.SimpleHTTPRequestHandler
    httpd = None

    while port < 8010:
        try:
            httpd = socketserver.TCPServer(("", port), handler)
            break
        except OSError:
            port += 1
    if not httpd: return

    def serve():
        httpd.serve_forever()

    threading.Thread(target=serve, daemon=True).start()
    webbrowser.open(f"http://localhost:{port}")
    print(f"📡 Galaxy active at port {port}. Closing in 5s...")
    time.sleep(5)

if __name__ == "__main__":
    args = sys.argv[1:]
    show_hidden = "-a" in args
    clean_args = [a for a in args if a != "-a"]
    
    path = clean_args[0] if clean_args else "."
    target_path = os.path.abspath(path)

    print(f"Scanning: {target_path} (All files: {show_hidden})")
    
    raw_tree = scan_system(target_path, max_depth=3, show_hidden=show_hidden)
    flat_nodes, flat_edges = build_bridge(raw_tree)
    
    generate_web_json(flat_nodes, flat_edges)
    start_ui()
