# 人格與經歷的資料格式與交換規則

## 初始人格（已實作）

保持原 JSON 格式，使用 `personadough.contract.validate_persona()` 驗證。

| 欄位 | 語意 |
|---|---|
| 基本資料.id | 十位小寫十六進位 ID，沿用既有格式 |
| 基本資料.姓名／年紀 | 角色基本資料；年紀為 0–120 整數 |
| 人格屬性.人格特質／社交能力／能力屬性 | 字串陣列；描述傾向，不等於心理量表分數 |
| 生平故事 | PersonaDough 產生的初始背景 |
| 語言行為／簡化行為 | 語言風格與人格摘要 |
| AI參數（可選） | 模型生成的參數建議，未驗證有效性 |

PersonaDough 是此資料的生產者。PsychAnchor 以角色 ID 關聯自己的問答、記憶與對話，不因一次行為更新原人格。

## 已有記憶

PsychAnchor 的 `rag/{persona_id}/qa_pairs.json` 儲存 `[{"q": "問題", "a": "回答"}]`，`index.faiss` 儲存問答向量；docs 由問答重建。

訪談回答由角色模型生成，應被理解為合成設定。它可能擴充角色經歷，但不是已觀測的人類事實。

## 後續經歷（設計，尚未實作）

將來可在 PsychAnchor 的 `experiences/{persona_id}.jsonl` 附加事件：

```json
{
  "schema_version": "1",
  "persona_id": "5c771e5f3c",
  "event_id": "由記憶系統產生",
  "source": "simulation",
  "observed_at": "含時區的時間",
  "situation": "參加聚會後感到疲累",
  "action": "提早回家休息",
  "outcome": "恢復精神",
  "story": "與朋友道別後回家，決定明天再約。"
}
```

事件、延伸故事、模型產生的解釋與錨定評估要分欄位，不能把模型解釋當作實際因果證據。錨定應在多次且相近情境下評估傾向；單次外向角色獨處不等於偏離。

## 儲存配置

三個 repo 使用相同的 `PERSONA_DATA_DIR` 絕對路徑；PsychAnchor 自己控制 `PSYCHANCHOR_DATA_DIR` 與 `CONVERSATION_DATA_DIR`；API 使用 `API_DATA_DIR` 存放環境／Unity 相關執行資料。

主 repo 僅提供整合入口，不成為角色資料的第二份真實來源。
