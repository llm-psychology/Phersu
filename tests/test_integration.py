import asyncio
import importlib.util
from pathlib import Path

def test_offline_cross_repository_flow():
    path=Path(__file__).resolve().parents[1]/"tools/offline_demo.py"
    spec=importlib.util.spec_from_file_location("offline_demo",path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert asyncio.run(module.run())
