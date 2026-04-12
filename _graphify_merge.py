import json
from pathlib import Path

ast = json.loads(Path(".graphify_ast.json").read_text())
sem = {"nodes": [], "edges": [], "hyperedges": []}

seen = {n["id"] for n in ast["nodes"]}
merged_nodes = list(ast["nodes"])
for n in sem["nodes"]:
    if n["id"] not in seen:
        merged_nodes.append(n)
        seen.add(n["id"])

merged_edges = ast["edges"] + sem["edges"]
merged_hyperedges = sem.get("hyperedges", [])
merged = {
    "nodes": merged_nodes,
    "edges": merged_edges,
    "hyperedges": merged_hyperedges,
    "input_tokens": 0,
    "output_tokens": 0,
}
Path(".graphify_extract.json").write_text(json.dumps(merged, indent=2))
total = len(merged_nodes)
edges = len(merged_edges)
print(
    "Merged: "
    + str(total)
    + " nodes, "
    + str(edges)
    + " edges ("
    + str(len(ast["nodes"]))
    + " AST + "
    + str(len(sem["nodes"]))
    + " semantic)"
)
