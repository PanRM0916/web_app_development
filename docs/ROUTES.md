# 路由設計 (Route Design) - 食譜收藏夾系統

本文件規劃了 Flask 應用的路由架構、對應模板與業務邏輯。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁 (食譜列表) | GET | `/` | `index.html` | 顯示所有食譜，支援關鍵字搜尋與分類篩選。 |
| 隨機挑選食譜 | GET | `/recipe/random` | — | 從資料庫隨機抽出一個 ID 並重導向至詳情頁。 |
| 新增食譜頁面 | GET | `/recipe/new` | `recipe_form.html` | 顯示結構化新增食譜的表單。 |
| 建立食譜 | POST | `/recipe/new` | — | 接收並驗證表單資料，存入資料庫後重導向至首頁。 |
| 食譜詳情頁 | GET | `/recipe/<int:id>` | `detail.html` | 顯示食譜完整資訊，包含食材換算與步驟互動。 |
| 編輯食譜頁面 | GET | `/recipe/<int:id>/edit` | `recipe_form.html` | 顯示帶有原有資料的編輯表單。 |
| 更新食譜 | POST | `/recipe/<int:id>/update` | — | 接收編輯後的資料，更新資料庫後重導向至詳情頁。 |
| 刪除食譜 | POST | `/recipe/<int:id>/delete` | — | 刪除指定食譜及其關聯資料，重導向至首頁。 |

---

## 2. 路由詳細說明

### 2.1 首頁 (Index)
- **輸入**: `q` (搜尋關鍵字, optional), `category` (分類過濾, optional)。
- **邏輯**: 呼叫 `Recipe.search()` 或 `Recipe.get_all()` 取得資料。
- **輸出**: 渲染 `index.html`。

### 2.2 隨機挑選 (Random)
- **邏輯**: 從 `Recipe.get_all()` 取得清單，隨機挑選一個 ID。
- **輸出**: 重導向至 `/recipe/<id>`。

### 2.3 新增/編輯食譜 (Form)
- **輸入**: `id` (僅編輯時需要)。
- **邏輯**: 
    - 新增：渲染空白表單。
    - 編輯：呼叫 `Recipe.get_by_id()` 取得資料並填入。
- **輸出**: 渲染 `recipe_form.html`。

### 2.4 建立/更新動作 (Action)
- **輸入**: 表單欄位 (`title`, `category`, `total_time`, `servings`, `ingredients[]`, `steps[]`, `tags[]`)。
- **邏輯**:
    - 驗證必填欄位 (標題、分類)。
    - 呼叫 `Recipe.create()` 或 `Recipe.update()`。
    - 處理食材與步驟的批次寫入。
- **輸出**: 成功則重導向；失敗則攜帶錯誤訊息返回表單。

---

## 3. Jinja2 模板清單

| 模板檔案 | 繼承模板 | 說明 |
| :--- | :--- | :--- |
| `layout.html` | — | 基礎佈局，包含 Navbar, Footer 與共用靜態資源。 |
| `index.html` | `layout.html` | 首頁，包含搜尋列、分類標籤與食譜卡片列表。 |
| `detail.html` | `layout.html` | 食譜內容頁，包含份量調整 JS 與步驟勾選功能。 |
| `recipe_form.html` | `layout.html` | 新增與編輯共用的表單頁面。 |

---

## 4. 路由骨架程式碼

路徑：`app/routes/recipe.py`
定義了所有與食譜管理相關的端點。
