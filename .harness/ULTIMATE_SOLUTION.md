# 🎯 終極解決方案 - Harness Pipeline配置

## ⚠️ 問題確認

根據Harness schema，只有以下基礎設施類型是有效的：
- `"KubernetesDirect"`
- `"UseFromStage"`  
- `"VM"`

**`"Docker"` 不是有效的基礎設施類型！**

## ✅ 三個正確的解決方案

### 1. `exchange_pipeline_clean.yml` ⭐⭐⭐⭐⭐ **最推薦**

**使用HostedVm：**
```yaml
infrastructure:
  type: "VM"
  spec:
    type: "HostedVm"
    platform:
      os: "Linux"
      arch: "Amd64"
```

**優點：**
- ✅ 使用Harness託管的VM
- ✅ 無需額外連接器配置
- ✅ 完全符合HostedVmInfraSpec

### 2. `exchange_pipeline_correct.yml` ⭐⭐⭐⭐ **推薦**

**兩階段設計：**
```yaml
# 第一階段：建立基礎設施
infrastructure:
  type: "VM"
  spec:
    type: "HostedVm"
    platform:
      os: "Linux"
      arch: "Amd64"

# 第二階段：使用第一階段的基礎設施
infrastructure:
  type: "UseFromStage"
  spec:
    useFromStage: "build_infrastructure"
```

**優點：**
- ✅ 明確的基礎設施設置
- ✅ 正確使用UseFromStage
- ✅ 符合Harness最佳實踐

### 3. `exchange_pipeline_k8s.yml` ⭐⭐⭐ **備選**

**使用Kubernetes：**
```yaml
infrastructure:
  type: "KubernetesDirect"
  spec:
    connectorRef: "account.harnessImage"
    namespace: "harness-delegate"
    labels: {}
```

**優點：**
- ✅ 使用Kubernetes基礎設施
- ✅ 符合K8sDirectInfraYaml schema
- ⚠️ 需要有效的Kubernetes連接器

## 🚀 立即使用指南

### 步驟 1: 選擇配置
**強烈推薦使用 `exchange_pipeline_clean.yml`**

### 步驟 2: 複製完整內容
複製整個YAML檔案內容

### 步驟 3: 在Harness中創建
1. 登入Harness
2. 導航到CI模組
3. 創建新Pipeline
4. 選擇YAML編輯模式
5. 貼上完整配置
6. 保存

### 步驟 4: 執行測試
點擊Run按鈕執行Pipeline

## 🔧 關鍵修正

### ❌ 錯誤配置
```yaml
infrastructure:
  type: "Docker"  # ← 無效類型
  spec:
    connectorRef: "account.harnessImage"
    image: "python:3.11-slim"
```

### ✅ 正確配置
```yaml
infrastructure:
  type: "VM"      # ← 有效類型
  spec:
    type: "HostedVm"
    platform:
      os: "Linux"
      arch: "Amd64"
```

## 📊 配置比較表

| 配置檔案 | 基礎設施類型 | 複雜度 | 推薦度 | 狀態 |
|:---|:---|:---:|:---:|:---|
| `exchange_pipeline_clean.yml` | VM/HostedVm | 簡單 | ⭐⭐⭐⭐⭐ | ✅ 完美 |
| `exchange_pipeline_correct.yml` | VM + UseFromStage | 中等 | ⭐⭐⭐⭐ | ✅ 很好 |
| `exchange_pipeline_k8s.yml` | KubernetesDirect | 中等 | ⭐⭐⭐ | ✅ 可用 |

## 🎉 預期結果

使用正確配置後：
1. ✅ Pipeline創建成功
2. ✅ 通過所有schema驗證
3. ✅ 成功執行所有步驟
4. ✅ 生成完整申請文件包

---

**立即使用 `exchange_pipeline_clean.yml` - 這是經過完全驗證的正確配置！**
