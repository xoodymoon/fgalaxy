import sys
import os
from map_fwalker import scan_system
from exporter import generate_web_json

def build_bridge(tree_data):
    nodes = []
    edges = []

    def flatten(node, parent_idx=None):
        current_idx = len(nodes)
        nodes.append({
            "name": node.get("name", "unknown"),
            "type": node.get("type", "file"),
            "path": node.get("path", "")
        })

        if parent_idx is not None:
            edges.append((parent_idx, current_idx))

        for child in node.get("children", []):
            flatten(child, current_idx)

    flatten(tree_data)
    return nodes, edges

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    
    target_path = os.path.abspath(path)
    print(f"Scanning target: {target_path}...")

    raw_tree = scan_system(target_path, max_depth=3)
    flat_nodes, flat_edges = build_bridge(raw_tree)
    
    generate_web_json(flat_nodes, flat_edges)
