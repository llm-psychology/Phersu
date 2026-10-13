"""No model calls: validate the shared data format using fixed responses."""
import asyncio
from pathlib import Path
import tempfile
from types import SimpleNamespace
from unittest.mock import AsyncMock
import numpy as np
from personadough.generator import CharacterGenerator
from psychanchor.persona_loader import PersonaLoader
from psychanchor.interviewer import Interviewer

async def run():
    with tempfile.TemporaryDirectory(prefix="persona-split-") as directory:
        root=Path(directory)
        generator=CharacterGenerator(use_ollama=True,output_dir=root/"personas")
        generator.story_generator.generate=AsyncMock(return_value="虛構展示角色喜歡閱讀並參與社區活動。")
        generator.tone_generator.generate=AsyncMock(return_value="自然、簡潔地表達。")
        generator.summarized_behavior_generator.generate=AsyncMock(return_value="這是離線資料流展示角色。")
        persona=await generator.generate_character_step()
        path=await generator.save_character(persona)
        loader=PersonaLoader(root/"personas")
        await loader.wait_until_ready()
        assert loader.get_persona_by_id(persona["基本資料"]["id"]) == persona
        interviewer=Interviewer()
        interviewer.rag_data_dir=str(root/"rag")
        qa=[{"q":"你的興趣是什麼？","a":"閱讀與社區活動。"}]
        vectors=np.array([[0.0,1.0]],dtype=np.float32)
        index=interviewer.build_vector_index(vectors)
        await interviewer.save_rag_database(persona["基本資料"]["id"],vectors,index,interviewer.format_qa_pairs(qa),qa)
        index,docs,_=await interviewer.load_rag_database(persona["基本資料"]["id"])
        interviewer.get_embedding_for_text=AsyncMock(return_value=SimpleNamespace(data=[SimpleNamespace(embedding=[0.0,1.0])]))
        retrieved,_=await interviewer.retrieve_similar_docs("你的興趣？",index,docs)
        interviewer.simulate_persona_answer=AsyncMock(return_value="我喜歡閱讀，也會参加社區活動。")
        answer=await interviewer.simulate_persona_answer(interviewer.build_simulation_prompt(persona,retrieved,"你的興趣？"))
        assert retrieved and answer
        print("PASS: PersonaDough JSON -> PsychAnchor loader -> FAISS save/load -> retrieval -> response")
        print("Fixed model responses and vectors; no OpenAI or Ollama requests were made.")
        return answer

if __name__=="__main__":
    asyncio.run(run())
