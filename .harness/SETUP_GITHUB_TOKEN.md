# 🔐 設置GitHub Personal Access Token (PAT)

## 📋 快速設置指南

按照以下步驟設置GitHub認證，解決Git push失敗問題。

---

## 步驟 1: 在GitHub生成Personal Access Token

### 1.1 前往GitHub Settings

1. 登入GitHub
2. 點擊右上角頭像 > **Settings**
3. 左側選單最下方 > **Developer settings**
4. 點擊 **Personal access tokens** > **Tokens (classic)**

### 1.2 生成新Token

1. 點擊 **Generate new token (classic)**
2. 填寫以下資訊：

| 欄位 | 值 |
|------|-----|
| **Note** | `Harness Pipeline - Exchange-Plan` |
| **Expiration** | 90 days （或 No expiration） |
| **Scopes** | ✅ **repo** (勾選所有子項目) |

3. 滑到最下方點擊 **Generate token**
4. **重要**: 複製生成的token（只會顯示一次！）

Token格式範例：
```
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 步驟 2: 在Harness中保存Token

### 2.1 前往Harness Secrets

1. 登入Harness
2. 前往您的**Project** (`exchange_plan`)
3. 左側選單 > **Project Settings**
4. 點擊 **Secrets**

### 2.2 創建新Secret

1. 點擊 **+ New Secret** > **Text**
2. 填寫以下資訊：

| 欄位 | 值 |
|------|-----|
| **Secret Name** | `github_pat` |
| **Description** | `GitHub Personal Access Token for Exchange-Plan push` |
| **Secret Value** | [貼上您剛複製的GitHub PAT] |

3. 點擊 **Save**

### 2.3 驗證Secret

確認：
- ✅ Secret名稱為 `github_pat`
- ✅ 值已正確保存
- ✅ 可以在Pipeline中引用

---

## 步驟 3: 驗證Pipeline配置

Pipeline已更新為使用這個token：

```yaml
- step:
    type: "Run"
    name: "Commit and Push Results to GitHub"
    identifier: "commit_push"
    spec:
      shell: "Bash"
      envVariables:
        GITHUB_TOKEN: <+secrets.getValue("github_pat")>  # ← 引用Secret
      command: |
        # Setup authentication
        git remote set-url origin https://${GITHUB_TOKEN}@github.com/National-Cheng-Chi-University-DCT-Dep/Exchange-Plan.git
        
        # Test authentication
        git ls-remote origin &> /dev/null && echo "✅ Auth OK" || echo "❌ Auth Failed"
        
        # Commit and push
        git add final_applications/
        git commit -m "..."
        git push origin HEAD:main
```

---

## 步驟 4: 測試執行

### 4.1 執行Pipeline

1. 在Harness中前往Pipeline
2. 點擊 **Run**
3. 選擇分支（通常是 `main`）
4. 執行

### 4.2 查看日誌

在 "Commit and Push Results to GitHub" 步驟中，應該看到：

```bash
✅ GitHub token configured
✅ Git authentication successful
Found final_applications directory with content!
Files to commit: [列表]
Pushing to GitHub...
✅ Successfully pushed generated documents to GitHub!
Branch: main
Commit: abc1234
```

### 4.3 驗證GitHub

1. 前往您的GitHub repository
2. 查看最新commits
3. 應該看到新的commit: `feat: Generate exchange application documents - [時間戳記]`
4. 檢查`final_applications/`目錄中的文件

---

## 🔧 疑難排解

### 問題 1: "GitHub token not configured"

**原因**: Harness找不到名為`github_pat`的secret

**解決方案**:
1. 檢查Secret名稱拼寫是否正確（`github_pat`）
2. 確認Secret在正確的Project中
3. 確認Secret的scope設置正確

### 問題 2: "Git authentication failed"

**原因**: Token無效或權限不足

**解決方案**:
1. 檢查Token是否過期
2. 確認Token有`repo`權限
3. 重新生成Token並更新Secret

### 問題 3: "Push failed - permission denied"

**原因**: Repository權限問題

**解決方案**:
1. 確認GitHub帳號對repository有write權限
2. 確認Token是由有權限的帳號生成
3. 檢查repository的branch protection rules

### 問題 4: "Files committed but not pushed"

**原因**: Token未配置或認證失敗

**解決方案**:
1. 文件已commit到本地，可以從Harness UI下載artifacts
2. 修正認證後重新執行Pipeline
3. 或者手動從Harness下載並push到GitHub

---

## 📊 Token權限說明

### 最小權限（推薦）

只需要 `repo` scope:
- ✅ `repo:status` - 讀取commit狀態
- ✅ `repo_deployment` - 訪問deployment
- ✅ `public_repo` - 訪問public repositories
- ✅ `repo:invite` - 訪問repository invitations
- ✅ **完整的`repo`權限** - 包含push權限

### 額外權限（可選）

如果需要其他功能：
- `workflow` - 更新GitHub Actions workflows
- `write:packages` - 發布packages
- `read:org` - 讀取組織信息

---

## 🎯 完整設置檢查清單

- [ ] 在GitHub生成Personal Access Token
- [ ] Token包含`repo`權限
- [ ] 複製Token（保存在安全的地方）
- [ ] 在Harness中創建Secret名為`github_pat`
- [ ] 貼上Token值
- [ ] 保存Secret
- [ ] 執行Pipeline測試
- [ ] 查看日誌確認"✅ Git authentication successful"
- [ ] 確認文件成功push到GitHub

---

## 💡 安全提示

1. **不要**將PAT commit到代碼庫中
2. **定期更新**PAT（建議90天）
3. **限制權限**：只給必要的scope
4. **使用Secret**：永遠通過Harness Secrets管理
5. **備份Token**：保存在密碼管理器中

---

## 🚀 設置完成後

一旦設置完成，Pipeline會：

1. ✅ 自動使用PAT認證
2. ✅ 測試連接是否成功
3. ✅ Commit生成的文件
4. ✅ Push到GitHub
5. ✅ 顯示commit hash

您只需要：
1. `git pull` 從GitHub獲取最新文件
2. 審閱生成的申請文件
3. 根據需要進行調整

---

**完成設置後，Pipeline就能自動保存所有生成的文件到GitHub了！** 🎉

