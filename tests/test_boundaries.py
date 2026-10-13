import ast
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

def test_dependency_direction():
    forbidden={"PersonaDough":{"psychanchor","persona_api","fastapi"},
               "PsychAnchor":{"persona_api","fastapi"}}
    for repo,names in forbidden.items():
        for path in (ROOT/repo/"src").rglob("*.py"):
            tree=ast.parse(path.read_text(encoding="utf-8-sig"))
            for node in ast.walk(tree):
                imports=[]
                if isinstance(node,ast.Import):
                    imports=[name.name for name in node.names]
                elif isinstance(node,ast.ImportFrom) and node.module:
                    imports=[node.module]
                assert not any(name.split('.')[0] in names for name in imports), str(path)
                if repo=="PsychAnchor":
                    assert "personadough.generator" not in imports, str(path)


def test_no_legacy_namespace_imports():
    for repo in ("PersonaDough","PsychAnchor","persona-api"):
        for path in (ROOT/repo/"src").rglob("*.py"):
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8-sig"))):
                if isinstance(node,ast.ImportFrom) and node.module and node.level == 0:
                    assert node.module.split('.')[0] not in {"module","interviewer","humanoid"}, str(path)
