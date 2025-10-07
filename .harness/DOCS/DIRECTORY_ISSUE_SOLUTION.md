# 🔍 目錄問題解決方案

## ⚠️ 問題描述

Pipeline執行時出現錯誤：
```
my_profile.yml not found
```

## 🔧 問題分析

這個問題通常由以下原因造成：

1. **工作目錄不正確** - Pipeline可能在錯誤的目錄中執行
2. **Git clone行為** - Harness可能將代碼clone到子目錄中
3. **文件路徑問題** - 相對路徑引用不正確

## ✅ 解決方案

### 方案 1: 使用修正後的Pipeline ⭐⭐⭐⭐⭐ **推薦**

**使用 `exchange_pipeline_verified.yml`** - 已修正所有步驟：

```yaml
# 每個步驟都包含目錄檢查和導航
if [ -d "Exchange-Plan" ]; then
  echo "Navigating to Exchange-Plan directory..."
  cd Exchange-Plan
fi
```

### 方案 2: 使用調試Pipeline 🔍 **調試用**

**使用 `exchange_pipeline_debug.yml`** - 專門用於診斷目錄問題：

- 顯示當前工作目錄
- 列出所有文件和目錄
- 檢查Exchange-Plan目錄是否存在
- 搜索所有.yml文件
- 顯示Git信息

## 🚀 執行步驟

### 步驟 1: 運行調試Pipeline
1. 在Harness中創建新Pipeline
2. 使用 `exchange_pipeline_debug.yml` 配置
3. 執行Pipeline
4. 查看輸出日誌

### 步驟 2: 分析結果
根據調試輸出：
- 如果找到 `Exchange-Plan/my_profile.yml` → 使用修正後的Pipeline
- 如果 `my_profile.yml` 在根目錄 → 問題可能是其他原因
- 如果都沒找到 → 檢查Git clone配置

### 步驟 3: 使用正確的Pipeline
根據調試結果選擇合適的Pipeline配置。

## 🔧 常見情況和對應解決方案

### 情況 1: 文件在 Exchange-Plan/ 子目錄中
```
✅ Found Exchange-Plan directory
✅ Found my_profile.yml in Exchange-Plan/
```
**解決方案**: 使用 `exchange_pipeline_verified.yml`

### 情況 2: 文件在根目錄中
```
✅ Found my_profile.yml in current directory
❌ Exchange-Plan directory not found
```
**解決方案**: 使用原始Pipeline配置（移除目錄導航代碼）

### 情況 3: 文件都不存在
```
❌ my_profile.yml not found in current directory
❌ Exchange-Plan directory not found
```
**解決方案**: 檢查Git連接器和repository配置

## 📊 修正後的Pipeline特點

### ✅ 智能目錄導航
```bash
# 自動檢測並導航到正確目錄
if [ -d "Exchange-Plan" ]; then
  echo "Navigating to Exchange-Plan directory..."
  cd Exchange-Plan
fi
```

### ✅ 詳細的錯誤報告
```bash
# 提供詳細的文件搜索信息
echo "Available files:"
find . -name "*.yml" -type f
```

### ✅ 目錄狀態顯示
```bash
# 顯示當前工作目錄
echo "Current directory: $(pwd)"
```

## 🎯 建議執行順序

1. **首先運行** `exchange_pipeline_debug.yml` 診斷問題
2. **根據結果選擇** 正確的Pipeline配置
3. **使用** `exchange_pipeline_verified.yml` 執行完整流程

---

**這個方法應該能完全解決目錄和文件路徑問題！**
