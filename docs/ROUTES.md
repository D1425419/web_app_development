# 讀書筆記本系統路由設計

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 書單首頁 | GET | `/` | `index.html` | 顯示所有書籍紀錄的列表 |
| 新增書籍頁面 | GET | `/books/create` | `form.html` | 顯示新增書籍的表單 |
| 建立書籍 | POST | `/books/create` | — | 接收表單資料，存入資料庫，並重導向至首頁 |
| 書籍詳情 | GET | `/books/<int:id>` | `detail.html` | 顯示單一書籍的完整內容與心得 |
| 編輯書籍頁面 | GET | `/books/<int:id>/edit` | `form.html` | 顯示載入既有書籍資料的編輯表單 |
| 更新書籍 | POST | `/books/<int:id>/update` | — | 接收表單更新資料，更新資料庫，並重導向至詳情頁 |
| 刪除書籍 | POST | `/books/<int:id>/delete` | — | 刪除書籍與封面圖片，並重導向至首頁 |

## 2. 每個路由的詳細說明

### 2.1 書單首頁 (`GET /`)
- **輸入**：無
- **處理邏輯**：呼叫 `BookModel.get_all_books()` 取得所有已儲存的書籍資料。
- **輸出**：將書籍資料列表作為變數傳入，並渲染 `index.html`。
- **錯誤處理**：若資料庫內沒有任何資料，模板應顯示友善提示，例如「目前沒有書籍紀錄，趕快新增第一本吧！」。

### 2.2 新增書籍頁面 (`GET /books/create`)
- **輸入**：無
- **處理邏輯**：準備要提供給前端渲染的預設變數（例如設定目前為「新增模式」）。
- **輸出**：渲染 `form.html`。
- **錯誤處理**：無。

### 2.3 建立書籍 (`POST /books/create`)
- **輸入**：
  - `request.form`: `title` (書名), `start_date` (開始日期), `end_date` (結束日期), `notes` (心得), `rating` (評分)
  - `request.files`: `cover_image` (封面圖片檔案)
- **處理邏輯**：
  1. 檢查並驗證必填欄位。
  2. 若有上傳圖片檔案，檢查格式與大小限制，然後儲存至 `static/uploads/` 目錄，並產生圖片的相對路徑。
  3. 將包含圖片路徑在內的所有資料交給 `BookModel.create_book(...)` 寫入資料庫。
- **輸出**：重導向至書單首頁 (`GET /`)。
- **錯誤處理**：若驗證失敗，重導向回新增頁面或直接渲染 `form.html` 並攜帶錯誤訊息 (flash)。

### 2.4 書籍詳情 (`GET /books/<int:id>`)
- **輸入**：URL 參數 `id` (書籍 ID)
- **處理邏輯**：呼叫 `BookModel.get_book_by_id(id)`。
- **輸出**：渲染 `detail.html` 並傳入書籍資料。
- **錯誤處理**：若查詢結果為 None（找不到該書），則回傳 HTTP 404 狀態碼及對應頁面。

### 2.5 編輯書籍頁面 (`GET /books/<int:id>/edit`)
- **輸入**：URL 參數 `id`
- **處理邏輯**：呼叫 `BookModel.get_book_by_id(id)` 取得該書籍現有資料。
- **輸出**：渲染 `form.html`（設定為「編輯模式」），並將既有資料填入表單。
- **錯誤處理**：若查無此書，回傳 404。

### 2.6 更新書籍 (`POST /books/<int:id>/update`)
- **輸入**：
  - URL 參數 `id`
  - `request.form` 及 `request.files` (與新增相同)
- **處理邏輯**：
  1. 呼叫 `BookModel.get_book_by_id(id)` 確認資料存在。
  2. 處理可能上傳的新封面圖片，如果有新圖片，則需更新路徑，也可一併刪除舊圖片檔案以節省空間。
  3. 呼叫 `BookModel.update_book(...)`。
- **輸出**：重導向至書籍詳情頁 (`GET /books/<id>`) 或首頁。
- **錯誤處理**：若查無此書回傳 404，驗證失敗處理方式同「建立書籍」。

### 2.7 刪除書籍 (`POST /books/<int:id>/delete`)
- **輸入**：URL 參數 `id`
- **處理邏輯**：
  1. 呼叫 `BookModel.get_book_by_id(id)` 取得資料（為了得知圖片路徑）。
  2. 刪除靜態資料夾中的封面圖片（如果存在）。
  3. 呼叫 `BookModel.delete_book(id)` 從資料庫刪除紀錄。
- **輸出**：重導向至首頁 (`GET /`)。
- **錯誤處理**：若查無此書回傳 404。

## 3. Jinja2 模板清單

所有的 HTML 檔案將放置於 `app/templates/` 目錄：

- `base.html`：基底模板，包含 `<head>`、Bootstrap (或其他 CSS 框架) CDN、共用的導覽列與頁尾。
- `index.html`：繼承自 `base.html`，以卡片或清單列表呈現所有書籍。
- `detail.html`：繼承自 `base.html`，展示單一書籍所有細節（包含大張封面圖片與心得全文）。
- `form.html`：繼承自 `base.html`，作為「新增」與「編輯」共用的表單視圖，會依據傳入變數改變標題與送出的 action URL。

## 4. 路由骨架程式碼

路由的骨架程式碼實作位於 `app/routes/book_routes.py`，並且使用 Flask 的 Blueprint 來進行模組化管理。
