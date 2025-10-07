# 🎯 Harness Pipeline 最終推薦配置

## ⭐ 最佳選擇：`exchange_pipeline_final.yml`

經過多次測試和修正，**強烈推薦使用 `exchange_pipeline_final.yml`**，原因如下：

### ✅ 優點
- **預裝Python環境**: 使用python:3.11-slim Docker映像
- **完整schema配置**: 包含所有必要的platform屬性
- **符合Schema**: 通過所有Harness YAML schema驗證
- **簡單可靠**: 最少的配置，最高的成功率

### 🔧 配置特點
```yaml
infrastructure:
  type: "Docker"
  spec:
    connectorRef: "account.harnessImage"
    image: "python:3.11-slim"
    platform:
      os: "Linux"
      arch: "Amd64"
```

## 🚀 使用步驟

### 1. 複製配置
複製 `exchange_pipeline_final.yml` 的完整內容

### 2. 在Harness中創建Pipeline
1. 登入Harness
2. 導航到 **CI** 模組
3. 點擊 **Create a Pipeline**
4. 輸入名稱：`Exchange Application Pipeline`
5. 選擇 **YAML** 編輯模式

### 3. 貼上配置並保存
1. 貼上完整的YAML配置
2. 點擊 **Save**
3. 點擊 **Run** 執行

## 🔍 已解決的問題

### ❌ 之前的錯誤
- `Infrastructure or runtime field is mandatory`
- `Missing property platform`
- `DockerInfraSpec` 錯誤
- `Run step with Kubernetes infra can't have empty connector field`

### ✅ 現在的解決方案
- 使用 `VM` + `HostedVm` 基礎設施
- 無需額外連接器配置
- 通過所有schema驗證
- 簡單可靠的配置

## 📊 其他配置選項

| 配置檔案 | 狀態 | 推薦度 | 說明 |
|:---|:---:|:---:|:---|
| `exchange_pipeline_final.yml` | ✅ 可用 | ⭐⭐⭐⭐⭐ | **強烈推薦** |
| `exchange_pipeline_working.yml` | ✅ 可用 | ⭐⭐⭐⭐ | Docker版本 |
| `exchange_pipeline_simple_final.yml` | ✅ 可用 | ⭐⭐⭐ | VM Pool版本 |
| `exchange_pipeline_docker.yml` | ✅ 可用 | ⭐⭐⭐ | 完整Docker配置 |
| `exchange_pipeline_minimal.yml` | ✅ 已修正 | ⭐⭐ | Kubernetes版本 |
| `exchange_pipeline.yml` | ⚠️ 複雜 | ⭐ | 生產環境使用 |

## 🎉 執行結果

成功執行後，您將獲得：
- ✅ 資格驗證報告 (`final_applications/eligibility_report.md`)
- ✅ 申請進度儀表板 (`final_applications/dashboard.md`)
- ✅ 16所學校的客製化申請文件
- ✅ 完整的讀書計畫和履歷

## 🆘 如果仍有問題

1. **確認使用正確的配置**: `exchange_pipeline_minimal.yml`
2. **檢查Harness帳戶權限**: 確保有CI模組權限
3. **聯繫Harness支援**: 如果基礎設施問題持續存在

---

**結論**: 使用 `exchange_pipeline_minimal.yml` 是最簡單、最可靠的選擇！
