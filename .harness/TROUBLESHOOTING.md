# 🔧 Pipeline 疑難排解指南

## ⚠️ 問題: "No final_applications directory found, nothing to commit"

### 問題描述
Pipeline執行完成，但在commit步驟顯示：
```
No final_applications directory found, nothing to commit
```

### 原因分析

這個問題表示文件生成步驟沒有成功創建文件。可能的原因：

#### 1. **Repository結構不匹配** 🔍
Pipeline期望的文件結構：
```
Exchange-Plan/
├── my_profile.yml
├── source_data/
│   ├── university_level_options.yml
│   └── college_level_options.yml
├── intelligence_gathering/
│   └── validator.py
└── build_scripts/
    └── generate_docs.py
```

但實際clone的repository可能有不同的結構（例如包含`schools.yml`而不是`university_level_options.yml`）

#### 2. **Python腳本執行失敗** ⚙️
- `validator.py` 或 `generate_docs.py` 執行時遇到錯誤
- 缺少必要的Python模組
- 配置文件格式錯誤

#### 3. **目錄權限問題** 🔒
- Pipeline無法創建`final_applications`目錄
- 無寫入權限

## ✅ 解決方案

### 方案 1: 檢查Pipeline日誌

查看**上一個階段**（Generate Application Documents）的詳細日誌：

```bash
# 應該看到以下輸出：
Generating application documents...
Current directory: /harness
Found document generator script
Ensured final_applications directory exists
Running document generator...
```

如果看到錯誤訊息，那就是問題所在。

### 方案 2: 確認Repository結構

在Pipeline的"Validate Configuration"步驟中查看：

```bash
# 應該顯示：
Current directory: /harness
Directory contents:
drwxr-xr-x ... build_scripts
drwxr-xr-x ... intelligence_gathering
-rw-r--r-- ... my_profile.yml
drwxr-xr-x ... source_data
```

如果您的repository結構不同，需要：
1. 確保運行Pipeline的是正確的repository
2. 或者調整Pipeline配置以適應您的repository結構

### 方案 3: 檢查Python腳本

Pipeline現在包含增強的診斷功能，會顯示：

```bash
# 如果找不到腳本：
ERROR: Document generator not found at build_scripts/generate_docs.py
Available build_scripts files:
[列出實際存在的文件]

# 如果找不到配置：
ERROR: my_profile.yml not found in current directory
Available .yml files:
[列出實際存在的.yml文件]
```

### 方案 4: 本地測試

在執行Pipeline之前，先在本地測試腳本：

```bash
cd Exchange-Plan

# 測試validator
python intelligence_gathering/validator.py

# 測試document generator
python build_scripts/generate_docs.py

# 檢查生成的文件
ls -la final_applications/
```

## 🔍 診斷步驟（已整合到Pipeline中）

更新後的Pipeline現在會自動：

### 1. **詳細的文件檢查**
```bash
# 搜索final_applications目錄
find . -name "final_applications" -type d

# 搜索生成的markdown文件
find . -name "*.md" -path "*/final_applications/*" -type f

# 顯示目錄內容
ls -la
```

### 2. **創建執行日誌**
如果沒有生成文件，Pipeline會自動創建`pipeline_logs/execution_summary.txt`並推送到GitHub，包含：
- Pipeline ID
- 執行時間
- 當前目錄
- 診斷建議

### 3. **顯示文件統計**
成功生成時會顯示：
```
Generated: X study plans, Y CV documents
Total files in final_applications: Z
Directory structure:
[列出所有生成的文件]
```

## 📋 常見情境和解決方法

### 情境 1: Repository是personal-publicdata而不是Exchange-Plan

**症狀**:
```
Available .yml files:
./source_data/schools.yml
./source_data/recommenders.yml
```

**解決方案**:
確認Harness中的GitHub connector指向正確的`Exchange-Plan` repository

### 情境 2: Python腳本存在但執行失敗

**症狀**:
```
Found document generator script
Running document generator...
[Python錯誤訊息]
```

**解決方案**:
1. 檢查Python腳本的錯誤訊息
2. 確認所有必要的Python模組已安裝
3. 驗證配置文件格式正確

### 情境 3: 文件生成但commit失敗

**症狀**:
```
Found final_applications directory with content!
Files to commit: [列出文件]
[Git錯誤訊息]
```

**解決方案**:
1. 檢查Git push權限
2. 確認GitHub connector配置正確
3. 檢查分支保護規則

## 🎯 下次執行前的檢查清單

- [ ] 確認運行的是`Exchange-Plan` repository
- [ ] 確認`my_profile.yml`存在且格式正確
- [ ] 確認`source_data/`目錄包含必要的配置文件
- [ ] 確認Python腳本可以在本地成功執行
- [ ] 確認GitHub connector有推送權限

## 📊 查看Pipeline執行結果

### 在Pipeline日誌中查找

1. **"Generate Application Documents"步驟**:
   - 查看是否成功創建目錄
   - 查看文件數量統計
   - 查看目錄結構列表

2. **"Commit and Push Results"步驟**:
   - 查看是否找到final_applications目錄
   - 查看Git add/commit/push的輸出
   - 確認commit hash

### 在GitHub上查看

1. 前往repository的commits頁面
2. 查找commit訊息包含"Generate exchange application documents"的commit
3. 查看changed files列表

## 🔄 Pipeline更新內容

最新版本的Pipeline包含以下改進：

✅ **增強的診斷功能**
- 詳細的目錄和文件檢查
- 自動搜索final_applications目錄
- 顯示完整的文件列表

✅ **更好的錯誤處理**
- 檢查目錄是否存在且非空
- 創建執行日誌即使生成失敗
- 詳細的錯誤訊息和建議

✅ **自動目錄創建**
- 確保final_applications目錄存在
- 創建pipeline_logs用於診斷

## 💡 提示

如果問題持續，您可以：

1. **直接在Harness中查看詳細日誌** - 每個步驟都有完整的輸出
2. **檢查pipeline_logs/execution_summary.txt** - 如果被創建並推送到GitHub
3. **在本地手動運行腳本** - 確認腳本本身沒有問題
4. **聯繫支援** - 提供Pipeline ID和執行時間

---

**記住：Pipeline現在會自動診斷問題並提供詳細信息！** 🚀

