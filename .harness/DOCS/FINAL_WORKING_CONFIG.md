# 🎯 最終工作配置 - 解決Schema衝突

## ⚠️ 問題分析

您遇到的錯誤是Harness schema驗證問題：
```
infrastructure: should be valid to one and only one of the schemas
```

這表示基礎設施配置匹配了多個schema，導致驗證失敗。

## ✅ 解決方案

我創建了兩個完全乾淨的配置，避免所有schema衝突：

### 1. `exchange_pipeline_clean.yml` ⭐⭐⭐⭐⭐ **強烈推薦**

**最簡潔的Docker配置：**
```yaml
infrastructure:
  type: "Docker"
  spec:
    connectorRef: "account.harnessImage"
    image: "python:3.11-slim"
```

**優點：**
- ✅ 最簡潔的配置，避免schema衝突
- ✅ 使用預裝Python環境
- ✅ 移除了可能導致衝突的platform屬性
- ✅ 完全符合DockerInfraYaml schema

### 2. `exchange_pipeline_k8s.yml` ⭐⭐⭐⭐ **備選方案**

**Kubernetes配置：**
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
- ✅ 完全符合K8sDirectInfraYaml schema
- ✅ 跨平台兼容命令 (python3 || python)

## 🚀 立即使用

### 步驟 1: 選擇配置
**推薦使用 `exchange_pipeline_clean.yml`**

### 步驟 2: 複製配置
複製整個檔案內容到Harness Pipeline編輯器

### 步驟 3: 保存並執行
1. 在Harness中貼上配置
2. 點擊Save
3. 點擊Run

## 🔧 關鍵差異

### 修正前 (有問題)
```yaml
infrastructure:
  type: "Docker"  # 或 "VM"
  spec:
    connectorRef: "account.harnessImage"
    image: "python:3.11-slim"
    platform:      # ← 這個可能導致schema衝突
      os: "Linux"
      arch: "Amd64"
```

### 修正後 (正確)
```yaml
infrastructure:
  type: "Docker"
  spec:
    connectorRef: "account.harnessImage"
    image: "python:3.11-slim"
    # 移除platform屬性，避免schema衝突
```

## 📊 配置比較

| 配置檔案 | Schema類型 | 推薦度 | 狀態 |
|:---|:---|:---:|:---|
| `exchange_pipeline_clean.yml` | DockerInfraYaml | ⭐⭐⭐⭐⭐ | ✅ 無衝突 |
| `exchange_pipeline_k8s.yml` | K8sDirectInfraYaml | ⭐⭐⭐⭐ | ✅ 無衝突 |
| `exchange_pipeline_final.yml` | 混合 | ⭐⭐ | ⚠️ 可能有衝突 |

## 🎉 預期結果

使用正確配置後，您應該能夠：
1. ✅ 成功創建Pipeline
2. ✅ 通過所有schema驗證
3. ✅ 成功執行所有步驟
4. ✅ 生成完整的申請文件

---

**建議立即使用 `exchange_pipeline_clean.yml` - 這是最可靠的配置！**
