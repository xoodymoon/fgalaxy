import os
from pathlib import Path

FILE_FAMILIES = {
    'code': ['.py', '.cpp', '.h', '.js', '.sh', '.html', '.css', '.lua'],
    '3d_creative': ['.blend', '.obj', '.fbx', '.unity', '.uasset'],
    'medical_data': ['.dicom', '.dcm', '.csv', '.xlsx', '.pdf'],
    'media': ['.jpg', '.png', '.mp4', '.mov', '.wav', '.mp3'],
    'config': ['.conf', '.yaml', '.json', '.toml', '.ini']
}

def get_file_family(extension):
    ext = extension.lower()
    for family, extensions in FILE_FAMILIES.items():
        if ext in extensions:
            return family
    return "generic"

def scan_system(target_path, max_depth=2):
    root = Path(target_path).resolve()
    
    def build_tree(current_path, depth):
        if depth > max_depth:
            return None
            
        is_dir = current_path.is_dir()
        node_type = "folder" if is_dir else "file"
        family = "folder" if is_dir else get_file_family(current_path.suffix)
        
        tree = {
            "name": current_path.name or str(current_path),
            "type": node_type,
            "family": family,
            "extension": current_path.suffix,
            "size": 0,
            "children": []
        }
        
        try:
            if is_dir:
                for item in current_path.iterdir():
                    if item.name.startswith('.'): continue
                    child_node = build_tree(item, depth + 1)
                    if child_node:
                        tree["children"].append(child_node)
                        tree["size"] += child_node["size"]
            else:
                tree["size"] = current_path.stat().st_size
        except PermissionError:
            return None
            
        return tree

    return build_tree(root, 0)

if __name__ == "__main__":
    structure = scan_system(".")
    print(f"Scanned: {structure['name']}")
    for child in structure['children']:
        print(f"  [{child['family'].upper()}] {child['name']}")

