# Harness Pipeline 配置說明

## 📋 檔案說明

### 1. `exchange_pipeline.yml` (完整版)
- **用途**: 完整的CI/CD流程，包含多個階段和複雜的配置
- **適用於**: 生產環境或需要詳細控制的情況
- **特點**: 
  - 分階段執行 (Validate → Generate → Quality Check → Notification)
  - 包含檔案上傳和存檔功能
  - 詳細的錯誤處理和通知機制

### 2. `exchange_pipeline_simple.yml` (簡化版) ⭐ **推薦**
- **用途**: 簡化的CI/CD流程，適合快速部署和測試
- **適用於**: 開發環境或快速原型驗證
- **特點**:
  - 單一階段執行所有步驟
  - 簡化的配置，易於理解和修改
  - 跨平台兼容 (支援 python3 和 python)

## 🚀 使用建議

### 對於初學者或快速開始
建議使用 `exchange_pipeline_simple.yml`，因為它：
- 配置簡單，容易理解
- 減少了配置錯誤的可能性
- 適合本地測試和開發

### 對於生產環境
如果需要更詳細的控制和監控，可以使用 `exchange_pipeline.yml`

## 🔧 配置要點

### 1. 連接器配置
在使用完整版Pipeline之前，需要配置以下連接器：
- `gcs_connector`: Google Cloud Storage連接器
- `harnessImage`: Harness映像連接器

### 2. 環境變數
確保以下環境變數已設置：
- `PYTHON_PATH`: Python執行路徑
- `PIP_PATH`: pip安裝路徑

### 3. 檔案權限
確保Harness有權限存取：
- 專案根目錄
- `final_applications/` 輸出目錄
- 所有Python腳本檔案

## 📝 自定義配置

### 修改執行命令
如果需要修改Python執行命令，可以編輯以下部分：
```yaml
command: |
  python3 intelligence_gathering/validator.py || python intelligence_gathering/validator.py
```

### 添加新的檢查步驟
可以在Quality Check階段添加新的檢查：
```yaml
- step:
    name: "Custom Check"
    identifier: "custom_check"
    type: "Run"
    spec:
      shell: "Bash"
      command: |
        # 您的自定義檢查邏輯
```

### 修改通知內容
可以編輯Success Notification步驟來自定義通知內容。

## 🐛 故障排除

### 常見問題

1. **Python命令找不到**
   - 確保Python已安裝並在PATH中
   - 使用完整路徑或配置環境變數

2. **檔案權限問題**
   - 檢查Harness執行用戶的權限
   - 確保可以寫入 `final_applications/` 目錄

3. **依賴套件問題**
   - 確保 `pyyaml` 已安裝
   - 可以在Setup Environment步驟中添加更多依賴

### 調試模式
在命令前添加 `set -x` 來啟用調試模式：
```yaml
command: |
  set -x
  python3 intelligence_gathering/validator.py
```

## 📚 相關資源

- [Harness CI/CD 文檔](https://docs.harness.io/category/ci)
- [Pipeline YAML 語法](https://docs.harness.io/article/3cx9u2p7as-pipeline-yaml-reference)
- [Step 類型參考](https://docs.harness.io/article/3cx9u2p7as-pipeline-yaml-reference#steps)

---

*此配置檔案為 ExchangeApp-IAC 專案的一部分*
