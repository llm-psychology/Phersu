import ast
import configparser
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def test_submodules_match_workspace_manifest():
    config = configparser.ConfigParser()
    config.read(ROOT / ".gitmodules", encoding="utf-8")
    manifest = json.loads((ROOT / "repositories.json").read_text(encoding="utf-8"))
    assert set(manifest) == {"PersonaDough", "PsychAnchor", "Phersu-api"}
    assert set(config.sections()) == {f'submodule "{name}"' for name in manifest}
    for name, entry in manifest.items():
        section = config[f'submodule "{name}"']
        assert section["path"] == name
        assert section["url"] == entry["url"] + ".git"
        assert section["branch"] == entry["ref"]
        assert (ROOT / entry["path"] / "pyproject.toml").is_file()

def test_dependency_direction():
    forbidden={"PersonaDough":{"psychanchor","persona_api","fastapi"},
               "PsychAnchor":{"persona_api","fastapi"}}
    for repo,names in forbidden.items():
        files = list((ROOT/repo/"src").rglob("*.py"))
        assert files, f"Missing submodule source: {repo}"
        for path in files:
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
    for repo in ("PersonaDough","PsychAnchor","Phersu-api"):
        files = list((ROOT/repo/"src").rglob("*.py"))
        assert files, f"Missing submodule source: {repo}"
        for path in files:
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8-sig"))):
                if isinstance(node,ast.ImportFrom) and node.module and node.level == 0:
                    assert node.module.split('.')[0] not in {"module","interviewer","humanoid"}, str(path)
