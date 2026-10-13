"""Verify already-built wheels installed in .wheel-smoke, without source imports."""
import importlib
import os
from pathlib import Path
import sys
import tempfile

target=Path(__file__).resolve().parents[1]/".wheel-smoke"
if not target.is_dir():
    raise SystemExit("Install the three wheels into .wheel-smoke first")
sys.path.insert(0,str(target))
with tempfile.TemporaryDirectory(prefix="persona-wheels-") as directory:
    root=Path(directory)
    for name,subdir in {"PERSONA_DATA_DIR":"personas","PSYCHANCHOR_DATA_DIR":"anchor",
                       "CONVERSATION_DATA_DIR":"conversations","API_DATA_DIR":"api"}.items():
        os.environ[name]=str(root/subdir)
    for package in ("personadough","psychanchor","persona_api"):
        module=importlib.import_module(package)
        assert Path(module.__file__).resolve().is_relative_to(target.resolve())
    from personadough.prompts import get_user_prompt
    assert "SENTINEL" in get_user_prompt("tone_generator",character_data="SENTINEL")
    from psychanchor.questions import QaLoader
    import asyncio
    async def load():
        loader=QaLoader()
        await loader.wait_until_ready()
        assert loader.get_question_count()>0
    asyncio.run(load())
    from fastapi.testclient import TestClient
    from persona_api.app import app
    with TestClient(app) as client:
        assert client.get("/health").status_code==200
        assert client.get("/").status_code==200
print("PASS: three installed wheels, prompts, interview questions, API and static resources")
