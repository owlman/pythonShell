import sys, json
from graphify.build import build_from_json
from graphify.cluster import score_all
from graphify.analyze import god_nodes, surprising_connections, suggest_questions
from graphify.report import generate
from pathlib import Path

extraction = json.loads(Path(".graphify_extract.json").read_text())
detection = json.loads(Path(".graphify_detect.json").read_text())
analysis = json.loads(Path(".graphify_analysis.json").read_text())

G = build_from_json(extraction)
communities = {int(k): v for k, v in analysis["communities"].items()}
cohesion = {int(k): v for k, v in analysis["cohesion"].items()}
tokens = {
    "input": extraction.get("input_tokens", 0),
    "output": extraction.get("output_tokens", 0),
}

labels = {
    0: "Integration Tests",
    1: "Project Scaffolding Tests",
    2: "Git Operations Tests",
    3: "SSH Operations Tests",
    4: "Pytest Fixtures",
    5: "RunCommand Tests",
    6: "SSH Key Configure Tests",
    7: "Mixed Test Utilities",
    8: "Core Common Module",
    9: "Git Pull Remote Tests",
    10: "Git Push Remote Tests",
    11: "Main Entry Point",
    12: "SSH Key Configure",
    13: "Create Book Project",
    14: "Create Translation Project",
    15: "Git Configuration",
    16: "Git Create Repository",
    17: "Git Pull Remote",
    18: "Git Push Remote",
    19: "Open SSH Proxy",
}

questions = suggest_questions(G, communities, labels)

report = generate(
    G,
    communities,
    cohesion,
    labels,
    analysis["gods"],
    analysis["surprises"],
    detection,
    tokens,
    ".",
)
Path("graphify-out/GRAPH_REPORT.md").write_text(report)
Path(".graphify_labels.json").write_text(
    json.dumps({str(k): v for k, v in labels.items()})
)
print("Report updated with community labels")
