# Deployment Guide
## GitHub Pages & CI/CD 整合部署指南

**更新日期**: 2025-10-07  
**狀態**: ✅ 完整整合完成

---

## 🎯 系統架構總覽

本專案整合了兩套CI/CD系統：

1. **GitHub Actions** - 主要自動化流程
2. **Harness Pipeline** - 企業級CI/CD整合

兩套系統可以獨立運作，也可以協同工作。

---

## 📐 架構圖

```
┌─────────────────────────────────────────────────────────────────┐
│                    Exchange-Plan Repository                      │
└────────┬─────────────────────────────────────────────────┬──────┘
         │                                                   │
         ├──────────────┐                         ┌─────────┴──────────┐
         │ GitHub       │                         │ Harness            │
         │ Actions      │                         │ Pipeline           │
         └──────┬───────┘                         └──────┬─────────────┘
                │                                        │
                │                                        │
        ┌───────▼────────────┐              ┌───────────▼────────────┐
        │ 1. Setup & Validate│              │ 1. Setup Environment   │
        │ 2. Generate Docs   │              │ 2. Generate Documents  │
        │ 3. Build Pages     │              │ 3. Build GitHub Pages  │
        │ 4. Deploy Pages    │              │ 4. Push to GitHub      │
        └───────┬────────────┘              └───────┬────────────────┘
                │                                   │
                └─────────┬─────────────────────────┘
                          │
                 ┌────────▼─────────┐
                 │  GitHub Pages    │
                 │  Static Website  │
                 └──────────────────┘
```

---

## 🚀 快速開始

### 方式一：使用 GitHub Actions（推薦）

#### 1. 啟用 GitHub Pages

在 GitHub Repository 設定中：

1. 前往 **Settings** → **Pages**
2. **Source**: Deploy from a branch
3. **Branch**: `main` / **Folder**: `/docs`
4. 點擊 **Save**

#### 2. 觸發工作流

```bash
# 方法 A: 推送變更（自動觸發）
git add .
git commit -m "feat: update application documents"
git push

# 方法 B: 手動觸發
# GitHub → Actions → Exchange Application CI/CD Pipeline → Run workflow
```

#### 3. 查看結果

- **Workflow**: `https://github.com/YOUR_USERNAME/Exchange-Plan/actions`
- **Website**: `https://YOUR_USERNAME.github.io/Exchange-Plan/`

---

### 方式二：使用 Harness Pipeline

#### 1. 設定 Harness

1. 在 Harness 中導入 pipeline 配置：
   - 原版: `.harness/Exchange-Plan/.harness/orgs/default/projects/default_project/exchange.yaml`
   - 整合版: `.harness/Exchange-Plan/.harness/orgs/default/projects/default_project/exchange-integrated.yaml`

2. 設定 Git Connector
3. 配置 Notifications (Email)

#### 2. 執行 Pipeline

1. 登入 Harness Platform
2. 選擇 Pipeline: **Exchange Application Integrated Pipeline**
3. 點擊 **Run**
4. 選擇 Branch
5. 執行

#### 3. Pipeline 會自動：

✅ 生成申請文件  
✅ 生成 GitHub Pages  
✅ 推送到 GitHub  
✅ 觸發 GitHub Actions 部署

---

## 📁 專案結構

```
Exchange-Plan/
├── .github/
│   └── workflows/
│       ├── exchange-app-pipeline.yml    # 主要 CI/CD workflow
│       └── pages-deploy.yml             # GitHub Pages 部署
│
├── .harness/
│   └── Exchange-Plan/.harness/orgs/default/projects/default_project/
│       ├── exchange.yaml                # 原始 Harness pipeline
│       └── exchange-integrated.yaml     # 整合版 Harness pipeline
│
├── build_scripts/
│   ├── generate_docs.py                 # 文件生成腳本
│   └── generate_pages.py                # GitHub Pages 生成腳本
│
├── docs/                                # GitHub Pages 靜態網站
│   ├── index.html                       # 主頁
│   ├── documents.html                   # 文件列表頁
│   ├── .nojekyll                        # 禁用 Jekyll
│   └── CNAME                            # 自訂域名（選用）
│
├── final_applications/                  # 生成的申請文件
│   ├── University_of_Bern/
│   │   ├── *_cv_*.md
│   │   └── *_study_plan_*.md
│   └── UC_San_Diego/
│       ├── *_cv_*.md
│       └── *_study_plan_*.md
│
└── templates/                           # 文件範本
    ├── cv_template.md
    ├── study_plan_template.md
    └── recommendation_request_template.md
```

---

## ⚙️ GitHub Actions Workflows

### 1. `exchange-app-pipeline.yml` - 主要 CI/CD

**觸發條件**:
- Push to `main` or `develop`
- 修改 `my_profile.yml`, `templates/**`, `build_scripts/**`
- 手動觸發

**Jobs**:
1. **setup-and-validate** - 環境設置與驗證
2. **generate-documents** - 生成申請文件
3. **build-github-pages** - 生成靜態網站
4. **deploy-github-pages** - 部署到 GitHub Pages
5. **notify-completion** - 完成通知

**使用方法**:
```bash
# 自動觸發
git add my_profile.yml
git commit -m "feat: update profile"
git push

# 手動觸發
# GitHub → Actions → Exchange Application CI/CD Pipeline → Run workflow
```

---

### 2. `pages-deploy.yml` - GitHub Pages 部署

**觸發條件**:
- Push to `main`
- 修改 `docs/**`
- 手動觸發

**Job**:
- **deploy** - 部署 `docs/` 到 GitHub Pages

---

## 🔄 工作流程

### 完整自動化流程

```
1. 修改 my_profile.yml
   ↓
2. Git commit & push
   ↓
3. GitHub Actions 觸發
   ↓
4. 生成申請文件（final_applications/）
   ↓
5. 生成 GitHub Pages（docs/）
   ↓
6. 自動 commit 並 push
   ↓
7. 部署到 GitHub Pages
   ↓
8. 🎉 網站更新完成！
```

---

### Harness + GitHub Actions 協同流程

```
1. Harness Pipeline 執行
   ↓
2. 生成文件與網頁
   ↓
3. 推送到 GitHub
   ↓
4. 觸發 GitHub Actions
   ↓
5. GitHub Actions 部署網站
   ↓
6. 🎉 完成！
```

---

## 🌐 GitHub Pages 配置

### 基本設定

在 `docs/` 目錄下：

1. **index.html** - 主頁，展示：
   - 個人資料摘要
   - GPA、IELTS 成績
   - 證照與獎項統計
   - 申請進度
   - 時間軸
   - 快速連結

2. **documents.html** - 文件列表頁

3. **.nojekyll** - 禁用 Jekyll 處理

4. **CNAME** - 自訂域名（選用）

### 自訂域名設定（選用）

如果有自己的域名：

1. 編輯 `docs/CNAME`:
   ```
   exchange.dennisleehappy.org
   ```

2. 在域名 DNS 設定中添加 CNAME 記錄:
   ```
   exchange  →  YOUR_USERNAME.github.io
   ```

3. GitHub 會自動配置 HTTPS

---

## 📊 監控與通知

### GitHub Actions 通知

工作流程完成後會顯示在：
- GitHub Actions 頁面
- Job Summary（詳細結果）

### Harness Pipeline 通知

配置了 Email 通知：
- **成功**: admin@dennisleehappy.org
- **失敗**: admin@dennisleehappy.org

---

## 🔧 進階配置

### 1. 修改生成腳本

編輯 `build_scripts/generate_pages.py` 來自訂網頁樣式與內容。

### 2. 添加新的 Workflow

在 `.github/workflows/` 新增 YAML 檔案：

```yaml
name: My Custom Workflow
on: [push]
jobs:
  my-job:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "Hello World"
```

### 3. 環境變數

在 GitHub Repository Settings → Secrets 添加：
- `PERSONAL_ACCESS_TOKEN` (如需要)
- 其他敏感資訊

---

## 🐛 故障排除

### 問題 1: GitHub Pages 沒有更新

**解決方案**:
1. 檢查 GitHub Pages 設定是否正確
2. 確認 `docs/` 目錄有檔案
3. 查看 Actions 頁面是否有錯誤
4. 清除瀏覽器快取

### 問題 2: Workflow 失敗

**解決方案**:
1. 查看 Actions 頁面的錯誤訊息
2. 檢查 `my_profile.yml` 語法是否正確
3. 確認 Python 腳本沒有錯誤

### 問題 3: 文件沒有生成

**解決方案**:
1. 本地測試:
   ```bash
   python build_scripts/generate_docs.py --all
   python build_scripts/generate_pages.py
   ```
2. 檢查錯誤訊息
3. 確認 `my_profile.yml` 格式正確

---

## 📝 最佳實踐

### 1. 版本控制

```bash
# 創建功能分支
git checkout -b feature/update-profile

# 修改並測試
# ... edit files ...

# 提交
git add .
git commit -m "feat: update personal profile"

# 推送並創建 PR
git push origin feature/update-profile
```

### 2. 本地測試

在推送前先本地測試：

```bash
# 測試文件生成
python build_scripts/generate_docs.py --all

# 測試網頁生成
python build_scripts/generate_pages.py

# 檢查生成結果
ls -la docs/
ls -la final_applications/
```

### 3. 定期更新

- 每週更新 `my_profile.yml`
- 添加新證照時立即記錄
- 重要成就及時補充

---

## 🎓 部署檢查清單

### 首次部署

- [ ] Fork/Clone repository
- [ ] 啟用 GitHub Pages（Settings → Pages）
- [ ] 設定 Branch 為 `main`，Folder 為 `/docs`
- [ ] 編輯 `my_profile.yml` 填入個人資訊
- [ ] 推送到 GitHub
- [ ] 等待 Actions 完成
- [ ] 訪問 GitHub Pages URL 確認

### 日常更新

- [ ] 更新 `my_profile.yml`
- [ ] 本地測試生成腳本
- [ ] Commit & Push
- [ ] 檢查 Actions 執行狀態
- [ ] 確認網站已更新

---

## 🔗 相關連結

- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **GitHub Pages Docs**: https://docs.github.com/en/pages
- **Harness Docs**: https://docs.harness.io/
- **PyYAML Docs**: https://pyyaml.org/

---

## 📧 支援

如遇問題：
1. 查看 GitHub Actions logs
2. 查看 Harness Pipeline logs
3. 檢查本文件的故障排除章節
4. 查閱 `INTEGRATION_GUIDE.md`

---

**最後更新**: 2025-10-07  
**狀態**: ✅ Production Ready  
**維護者**: AI Assistant + Pei-Chen Lee

🎉 **恭喜！您的 Exchange Application System 已完全自動化並部署到 GitHub Pages！**

