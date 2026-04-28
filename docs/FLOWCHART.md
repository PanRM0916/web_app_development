# 流程圖設計 (Flowcharts) - 食譜收藏夾系統

本文件根據 PRD 與系統架構文件產出，視覺化呈現使用者操作路徑與系統資料流。

## 1. 使用者流程圖 (User Flow)

描述使用者在系統中的操作邏輯與頁面跳轉。

```mermaid
flowchart LR
  Start([使用者開啟網頁]) --> Home[首頁 - 食譜列表]
  
  Home --> Search{搜尋或篩選？}
  Search -->|是| FilteredHome[顯示過濾後的列表]
  Search -->|否| Home
  
  Home --> Action{執行什麼操作？}
  
  Action -->|新增食譜| CreateForm[新增食譜表單頁]
  CreateForm --> Submit[填寫並送出]
  Submit --> Home
  
  Action -->|查看詳情| Detail[食譜詳情頁]
  Detail --> Adjust[調整份量 / 標記步驟]
  Adjust --> Detail
  
  Action -->|今天吃什麼| Random[隨機推薦功能]
  Random --> Detail
```

---

## 2. 系統序列圖 (Sequence Diagram)

以「新增食譜」功能為例，描述資料在各層級間的流動。

```mermaid
sequenceDiagram
  actor User as 使用者
  participant Browser as 瀏覽器
  participant Route as Flask Route
  participant Model as Model (Data Logic)
  participant DB as SQLite 資料庫

  User->>Browser: 填寫食譜資訊並點擊送出
  Browser->>Route: POST /recipe/new
  Route->>Model: 呼叫儲存邏輯 (驗證資料)
  Model->>DB: 執行 INSERT INTO recipes
  DB-->>Model: 回傳成功
  Model-->>Route: 回傳處理結果
  Route-->>Browser: HTTP 302 重導向至 / (首頁)
  Browser->>Route: GET /
  Route->>Model: 查詢最新食譜列表
  Model->>DB: SELECT * FROM recipes
  DB-->>Model: 回傳列表資料
  Model-->>Route: 回傳食譜物件清單
  Route-->>Browser: 渲染首頁 HTML
  Browser-->>User: 顯示更新後的食譜列表
```

---

## 3. 功能清單對照表

| 功能描述 | URL 路徑 | HTTP 方法 | 職責說明 |
| :--- | :--- | :--- | :--- |
| **食譜列表** | `/` | GET | 顯示所有食譜，支援關鍵字搜尋與分類/標籤篩選。 |
| **新增頁面** | `/recipe/new` | GET | 呈現結構化新增食譜的互動表單。 |
| **執行新增** | `/recipe/new` | POST | 接收表單資料，建立食譜、食材與步驟記錄。 |
| **詳情預覽** | `/recipe/<int:id>` | GET | 顯示食譜完整資訊，包含份量轉換與步驟勾選互動。 |
| **隨機挑選** | `/recipe/random` | GET | 從資料庫隨機抽取一個 ID 並重導向至詳情頁。 |
