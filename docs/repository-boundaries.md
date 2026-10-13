# 模組邊界

| Repo | 負責內容 | 輸出 |
|---|---|---|
| PersonaDough | 基本資料、人格特質、初始背景故事與語言風格 | 人格 JSON |
| PsychAnchor | 訪談、記憶檢索、回答與情境決策 | 訪談索引、對話與決策 |
| persona-api | HTTP、SSE、背景任務、模擬環境及展示頁面 | API 與事件串流 |
| persona-platform | 導覽、資料格式與跨 repo 整合驗證 | 開發入口 |

依賴方向為 `persona-api → psychanchor → personadough`，API 也可直接使用 PersonaDough。

PsychAnchor 只重用 PersonaDough 的 JSON 驗證、路徑設定與模型 adapter，不呼叫人格生成器。初始人格保持固定；訪談記憶與後續經歷另存。量化人格錨定、偏離評估／校正與後續故事生成尚未完成。

API 的模擬環境負責執行行動，PsychAnchor 負責產生角色決策。API 仍有全域狀態及原型技術債，尚未支援正式多租戶部署。

拆分前的原型與 Git 歷史另存於 [PersonaDough-archive](https://github.com/llm-psychology/PersonaDough-archive)。
