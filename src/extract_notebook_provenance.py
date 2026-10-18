"""Extract edge-level provenance notes from the original construction notebook.

The extractor is intentionally conservative. It reads active ``add_edge`` calls,
their adjacent comments, and the ``compose_all`` statements used to build the
deposited networks. It never treats a nearby document as proof by itself.
"""

from __future__ import annotations

import argparse
import ast
import csv
import json
import re
import unicodedata
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import networkx as nx


REFERENCE_RE = re.compile(r"(?<![A-Za-z0-9])(?:n\d{1,3}|AV\s*pg(?:ch)?\s*\d+)(?![A-Za-z0-9])", re.I)
TOKEN_RE = re.compile(r"[a-z0-9]+")
STOPWORDS = {
    "a", "al", "ante", "caso", "con", "contra", "de", "del", "el", "en",
    "la", "las", "lo", "los", "para", "por", "que", "se", "su", "un", "una",
}


@dataclass(frozen=True)
class EdgeStatement:
    notebook: str
    graph: str
    source: str
    target: str
    cell: int
    line: int
    comment: str
    reference_tokens: tuple[str, ...]


def normalize_text(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value)
    ascii_text = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return " ".join(TOKEN_RE.findall(ascii_text.lower()))


def informative_tokens(value: str) -> set[str]:
    return {
        token for token in normalize_text(value).split()
        if len(token) >= 4 and token not in STOPWORDS
    }


def sanitize_python(source: str) -> str:
    lines = []
    for line in source.splitlines():
        if line.lstrip().startswith(("!", "%")):
            lines.append("# " + line)
        else:
            lines.append(line)
    return "\n".join(lines)


def adjacent_comments(lines: list[str], lineno: int) -> str:
    index = lineno - 1
    notes: list[str] = []

    current = lines[index] if 0 <= index < len(lines) else ""
    if "#" in current:
        trailing = current.split("#", 1)[1].strip()
        if trailing:
            notes.append(trailing)

    before: list[str] = []
    for candidate in reversed(lines[max(0, index - 8):index]):
        stripped = candidate.strip()
        if not stripped:
            if before:
                break
            continue
        if not stripped.startswith("#"):
            break
        before.append(stripped.lstrip("#").strip())
    notes = list(reversed(before)) + notes

    for candidate in lines[index + 1:min(len(lines), index + 7)]:
        stripped = candidate.strip()
        if not stripped:
            break
        if not stripped.startswith("#"):
            break
        notes.append(stripped.lstrip("#").strip())

    unique: list[str] = []
    for note in notes:
        if note and note not in unique:
            unique.append(note)
    return " | ".join(unique)


def string_constant(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def parse_notebook(path: Path) -> tuple[list[EdgeStatement], dict[str, list[str]], dict[str, str]]:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    statements: list[EdgeStatement] = []
    compositions: dict[str, list[str]] = {}
    outputs: dict[str, str] = {}

    for cell_index, cell in enumerate(notebook.get("cells", [])):
        if cell.get("cell_type") != "code":
            continue
        source = "".join(cell.get("source", []))
        sanitized = sanitize_python(source)
        lines = sanitized.splitlines()
        try:
            tree = ast.parse(sanitized)
        except SyntaxError:
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                owner = node.func.value
                if node.func.attr == "add_edge" and isinstance(owner, ast.Name) and len(node.args) >= 2:
                    source_node = string_constant(node.args[0])
                    target_node = string_constant(node.args[1])
                    if source_node is None or target_node is None:
                        continue
                    comment = adjacent_comments(lines, node.lineno)
                    refs = tuple(dict.fromkeys(match.group(0).replace(" ", "") for match in REFERENCE_RE.finditer(comment)))
                    statements.append(
                        EdgeStatement(
                            notebook=path.name,
                            graph=owner.id,
                            source=source_node,
                            target=target_node,
                            cell=cell_index,
                            line=node.lineno,
                            comment=comment,
                            reference_tokens=refs,
                        )
                    )
                elif node.func.attr == "write_gexf" and len(node.args) >= 2:
                    graph_arg = node.args[0]
                    file_arg = string_constant(node.args[1])
                    if isinstance(graph_arg, ast.Name) and file_arg:
                        outputs[Path(file_arg).name] = graph_arg.id

            if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                value = node.value
                if not (
                    isinstance(value, ast.Call)
                    and isinstance(value.func, ast.Attribute)
                    and value.func.attr == "compose_all"
                    and value.args
                    and isinstance(value.args[0], (ast.List, ast.Tuple))
                ):
                    continue
                components = [item.id for item in value.args[0].elts if isinstance(item, ast.Name)]
                compositions[node.targets[0].id] = components

    return statements, compositions, outputs


def canonical_edge(source: str, target: str) -> tuple[str, str]:
    return tuple(sorted((str(source), str(target)), key=str.casefold))


def load_source_inventory(path: Path | None) -> list[str]:
    if path is None or not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return [row["archive_path"] for row in csv.DictReader(stream) if row.get("archive_path")]


def candidate_documents(comment: str, documents: list[str]) -> list[str]:
    note_tokens = informative_tokens(comment)
    if len(note_tokens) < 2:
        return []
    scored: list[tuple[float, str]] = []
    for document in documents:
        title_tokens = informative_tokens(Path(document).stem)
        if len(title_tokens) < 2:
            continue
        overlap = note_tokens & title_tokens
        if len(overlap) < 2:
            continue
        score = len(overlap) / min(len(note_tokens), len(title_tokens))
        if score >= 0.45:
            scored.append((score, document))
    scored.sort(key=lambda item: (-item[0], item[1].casefold()))
    return [document for _, document in scored[:3]]


def collect_records(
    notebook_paths: list[Path],
    network_dir: Path,
    source_inventory: Path | None,
) -> tuple[list[dict[str, str]], list[EdgeStatement], dict[str, object]]:
    statements: list[EdgeStatement] = []
    parsed_notebooks: dict[str, dict[str, object]] = {}
    for notebook_path in notebook_paths:
        notebook_statements, compositions, outputs = parse_notebook(notebook_path)
        statements.extend(notebook_statements)
        parsed_notebooks[notebook_path.name] = {
            "active_add_edge_statements": len(notebook_statements),
            "compositions": compositions,
            "outputs": outputs,
        }

    candidates: dict[tuple[str, str], list[EdgeStatement]] = defaultdict(list)
    for statement in statements:
        candidates[canonical_edge(statement.source, statement.target)].append(statement)

    documents = load_source_inventory(source_inventory)
    rows: list[dict[str, str]] = []
    summary: dict[str, object] = {
        "notebooks": parsed_notebooks,
        "active_add_edge_statements": len(statements),
        "networks": {},
    }

    for network_path in sorted(network_dir.glob("*.gexf")):
        graph = nx.read_gexf(network_path)
        matched = 0
        for source, target in graph.edges():
            key = canonical_edge(source, target)
            provenance = candidates.get(key, [])
            if provenance:
                matched += 1
            comments = list(dict.fromkeys(item.comment for item in provenance if item.comment))
            refs = list(dict.fromkeys(ref for item in provenance for ref in item.reference_tokens))
            docs = list(dict.fromkeys(doc for comment in comments for doc in candidate_documents(comment, documents)))
            rows.append(
                {
                    "network": network_path.name,
                    "source": str(source),
                    "target": str(target),
                    "match_status": "matched_active_notebook_statement" if provenance else "not_found_in_supplied_notebooks",
                    "notebook_files": "|".join(dict.fromkeys(item.notebook for item in provenance)),
                    "graph_components": "|".join(dict.fromkeys(item.graph for item in provenance)),
                    "notebook_locations": "|".join(
                        dict.fromkeys(f"{item.notebook}:cell{item.cell}:line{item.line}" for item in provenance)
                    ),
                    "evidence_notes": " || ".join(comments),
                    "reference_tokens": "|".join(refs),
                    "candidate_source_documents": "|".join(docs),
                    "candidate_status": "unverified_title_match" if docs else "",
                }
            )

        summary["networks"][network_path.name] = {
            "nodes": graph.number_of_nodes(),
            "edges": graph.number_of_edges(),
            "matched_edges": matched,
            "unmatched_edges": graph.number_of_edges() - matched,
        }
    return rows, statements, summary


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0]) if rows else []
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_composition_audit(notebook_paths: list[Path], network_dir: Path) -> list[dict[str, str]]:
    deposited: dict[str, set[tuple[str, str]]] = {}
    for network_path in sorted(network_dir.glob("*.gexf")):
        graph = nx.read_gexf(network_path)
        deposited[network_path.name] = {canonical_edge(source, target) for source, target in graph.edges()}

    rows: list[dict[str, str]] = []
    for notebook_path in notebook_paths:
        statements, compositions, outputs = parse_notebook(notebook_path)
        by_graph: dict[str, set[tuple[str, str]]] = defaultdict(set)
        for statement in statements:
            by_graph[statement.graph].add(canonical_edge(statement.source, statement.target))
        output_by_graph = {graph_name: file_name for file_name, graph_name in outputs.items()}
        for composition_name, components in compositions.items():
            constructed: set[tuple[str, str]] = set()
            for component in components:
                constructed.update(by_graph.get(component, set()))
            network_name = output_by_graph.get(composition_name, "")
            final_edges = deposited.get(network_name)
            intersection = constructed & final_edges if final_edges is not None else set()
            union = constructed | final_edges if final_edges is not None else set()
            rows.append(
                {
                    "notebook": notebook_path.name,
                    "composition_graph": composition_name,
                    "components": "|".join(components),
                    "declared_output": network_name,
                    "output_present": "yes" if final_edges is not None else "no",
                    "constructed_edges": str(len(constructed)),
                    "deposited_edges": str(len(final_edges)) if final_edges is not None else "",
                    "matched_edges": str(len(intersection)) if final_edges is not None else "",
                    "notebook_only_edges": str(len(constructed - final_edges)) if final_edges is not None else "",
                    "gexf_only_edges": str(len(final_edges - constructed)) if final_edges is not None else "",
                    "jaccard": f"{len(intersection) / len(union):.6f}" if union else "",
                }
            )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    notebook_group = parser.add_mutually_exclusive_group(required=True)
    notebook_group.add_argument("--notebook", type=Path, action="append")
    notebook_group.add_argument("--notebook-dir", type=Path)
    parser.add_argument("--network-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--source-inventory", type=Path)
    args = parser.parse_args()

    notebook_paths = args.notebook or sorted(args.notebook_dir.glob("*.ipynb"))
    if not notebook_paths:
        parser.error("No notebooks found")
    rows, statements, summary = collect_records(
        notebook_paths,
        args.network_dir,
        args.source_inventory,
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.output_dir / "edges_provenance.csv", rows)
    write_csv(
        args.output_dir / "notebook_edge_statements.csv",
        [
            {
                "notebook": item.notebook,
                "graph": item.graph,
                "source": item.source,
                "target": item.target,
                "cell": str(item.cell),
                "line": str(item.line),
                "evidence_notes": item.comment,
                "reference_tokens": "|".join(item.reference_tokens),
            }
            for item in statements
        ],
    )
    audit_rows = build_composition_audit(notebook_paths, args.network_dir)
    if audit_rows:
        write_csv(args.output_dir / "notebook_reconstruction_audit.csv", audit_rows)
    (args.output_dir / "provenance_extraction_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
