# 讀書筆記本系統流程圖

## 1. 使用者流程圖 (User Flow)

這張圖描述了使用者在讀書筆記本系統中的操作路徑。

```mermaid
flowchart LR
    A([使用者進入網站]) --> B[首頁 - 書單列表]
    B --> C{選擇操作}
    
    C -->|新增書籍| D[點擊新增書籍按鈕]
    D --> E[填寫書籍資訊表單]
    E --> F{是否上傳封面？}
    F -->|是| G[選擇圖片檔案]
    F -->|否| H[送出表單]
    G --> H
    H --> I[系統儲存成功]
    I --> B
    
    C -->|查看/編輯/刪除| J[點擊特定書籍]
    J --> K[進入書籍編輯/詳情頁面]
    K --> L{選擇操作}
    L -->|編輯| M[修改書名、心得、評分、時間等]
    M --> N[送出修改]
    N --> I
    L -->|刪除| O[點擊刪除按鈕]
    O --> P[確認刪除]
    P --> Q[系統刪除成功]
    Q --> B
    L -->|返回| B
```

## 2. 系統序列圖 (Sequence Diagram)

這張圖描述了從「使用者提交新增書籍表單」到「資料存入資料庫」並返回畫面的完整後端處理流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask Route (book_routes)
    participant Model as Model (book_model)
    participant DB as SQLite 資料庫
    
    User->>Browser: 填寫書籍表單(書名、封面、心得等)並送出
    Browser->>Route: POST /books/create
    
    Route->>Route: 驗證表單資料
    
    alt 包含圖片上傳
        Route->>Route: 檢查圖片格式與大小
        Route->>Route: 儲存圖片至 static/uploads/
    end
    
    Route->>Model: 呼叫新增書籍函式 (傳遞資料與圖片路徑)
    Model->>DB: INSERT INTO books ...
    DB-->>Model: 執行成功
    Model-->>Route: 回傳成功狀態
    
    Route-->>Browser: HTTP 302 重導向至首頁
    Browser->>Route: GET /
    Route->>Model: 呼叫取得書籍列表函式
    Model->>DB: SELECT * FROM books
    DB-->>Model: 回傳查詢結果
    Model-->>Route: 回傳書籍資料列表
    Route-->>Browser: 將資料傳遞給 Jinja2 渲染 index.html 並顯示
```

## 3. 功能清單對照表

| 功能名稱 | 說明 | URL 路徑 | HTTP 方法 | 對應的 View (模板) |
| --- | --- | --- | --- | --- |
| **首頁/書單列表** | 顯示所有已記錄的書籍列表 | `/` 或 `/books` | `GET` | `index.html` |
| **新增書籍表單** | 顯示新增書籍的輸入表單 | `/books/create` | `GET` | `form.html` |
| **儲存新增書籍** | 接收表單資料，儲存圖片與資料庫紀錄 | `/books/create` | `POST` | (重導向至 `/`) |
| **編輯書籍表單** | 顯示修改書籍資料的表單 (帶有預設值) | `/books/<id>/edit` | `GET` | `form.html` |
| **更新書籍資料** | 接收修改後的資料並更新至資料庫 | `/books/<id>/edit` | `POST` | (重導向至 `/`) |
| **刪除書籍** | 刪除指定的書籍紀錄與關聯圖片 | `/books/<id>/delete` | `POST` | (重導向至 `/`) |
