# Harness Pipeline 快速開始指南

## 🚀 立即開始

### 步驟 1: 選擇Pipeline配置
根據您的需求選擇以下配置之一：

| 配置檔案 | 推薦程度 | 適用情況 |
|:---|:---:|:---|
| `exchange_pipeline_hosted.yml` | ⭐⭐⭐⭐⭐ | 初學者、快速測試 |
| `exchange_pipeline_vm.yml` | ⭐⭐⭐⭐ | 需要VM基礎設施 |
| `exchange_pipeline_docker.yml` | ⭐⭐⭐ | 需要特定Python環境 |
| `exchange_pipeline_ubuntu.yml` | ⭐⭐ | 需要完整Linux環境 |
| `exchange_pipeline.yml` | ⭐⭐ | 生產環境、複雜需求 |

### 步驟 2: 在Harness中創建Pipeline

1. 登入您的Harness帳戶
2. 導航到 **CI** 模組
3. 點擊 **Create a Pipeline**
4. 輸入Pipeline名稱：`Exchange Application Pipeline`
5. 選擇 **YAML** 編輯模式

### 步驟 3: 貼上配置內容

複製選定的YAML檔案內容並貼到Pipeline配置中。

### 步驟 4: 保存並執行

1. 點擊 **Save** 保存Pipeline
2. 點擊 **Run** 執行Pipeline
3. 等待執行完成並查看結果

## ⚡ 推薦配置：`exchange_pipeline_hosted.yml`

這是**最簡單**的配置，適合大多數使用者：

```yaml
# 使用 Harness 託管基礎設施
infrastructure:
  type: "VM"
  spec:
    type: "HostedVm"
```

### 優點：
- ✅ 無需額外配置連接器
- ✅ 使用Harness託管的VM環境
- ✅ 自動處理基礎設施管理
- ✅ 適合快速測試和驗證

## 🔧 故障排除

### 問題 1: "Infrastructure or runtime field is mandatory"
**解決方案**: 確保Pipeline配置中包含基礎設施配置，使用 `exchange_pipeline_hosted.yml`

### 問題 2: "Missing property platform" 或 "DockerInfraSpec"
**解決方案**: 使用 `exchange_pipeline_hosted.yml` 或 `exchange_pipeline_vm.yml` 避免Docker配置問題

### 問題 3: "Connector not found"
**解決方案**: 使用 `exchange_pipeline_hosted.yml` 避免需要額外連接器

### 問題 4: "Python command not found"
**解決方案**: 
- 使用 `exchange_pipeline_docker.yml` (預裝Python)
- 或在Setup Environment步驟中安裝Python

### 問題 5: "Permission denied"
**解決方案**: 檢查Harness帳戶權限和專案設置

## 📊 執行結果

成功執行後，您應該會看到：

```
==========================================
交換申請文件生成完成！
==========================================
生成時間: 2025-10-07 10:57:36
文件位置: final_applications/
儀表板: final_applications/dashboard.md

下一步建議:
1. 檢查各校申請截止日期
2. 準備英語檢定成績
3. 聯繫推薦人撰寫推薦信

---
此通知由 ExchangeApp-IAC 自動發送
==========================================
```

## 🎯 下一步

1. 檢查生成的申請文件
2. 根據各校要求調整內容
3. 準備其他必要文件 (推薦信、成績單等)
4. 提交申請

---

*需要幫助？請參考 `.harness/README.md` 獲取詳細說明*
