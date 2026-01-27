import json
import os

def generate_web_json(nodes, edges):
    project_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(project_dir, "map_data.json")

    web_data = {
        "nodes": [],
        "links": []
    }

    for i, node in enumerate(nodes):
        _, ext = os.path.splitext(node['name'])

        web_data["nodes"].append({
            "id": i,
            "name": node['name'],
            "type": node['type'],
            "family": node.get('family', 'generic'),
            "ext": ext.lower()
        })

    for source, target in edges:
        web_data["links"].append({
            "source": source,
            "target": target
        })

    with open(output_path, "w") as f:
        json.dump(web_data, f, indent=4)
        
    print(f"📁 Data saved to: {output_path}")
