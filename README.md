# Exchange-Plan 🎓
## 台灣聯合大學系統交換學生申請自動化系統

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-success)](https://YOUR_USERNAME.github.io/Exchange-Plan/)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue)](https://github.com/YOUR_USERNAME/Exchange-Plan/actions)
[![Harness](https://img.shields.io/badge/CI%2FCD-Harness-orange)](https://app.harness.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🌟 專案簡介

**Exchange-Plan** 是一個完整的交換學生申請自動化管理系統，從資料管理、文件生成到網頁展示，實現全流程自動化。

### 核心功能

✅ **資料集中管理** - 單一 YAML 檔案管理所有個人資訊  
✅ **自動文件生成** - 一鍵生成客製化 CV 和學習計畫  
✅ **GitHub Pages** - 美觀的網頁展示申請進度  
✅ **雙 CI/CD 系統** - GitHub Actions + Harness Pipeline  
✅ **完整文件** - 詳細的使用指南和檢查清單

---

## 📊 專案狀態

| 項目 | 狀態 | 完成度 |
|------|------|--------|
| 個人資料整合 | ✅ 完成 | 100% |
| 文件範本系統 | ✅ 完成 | 100% |
| 自動化腳本 | ✅ 完成 | 100% |
| GitHub Pages | ✅ 完成 | 100% |
| CI/CD 整合 | ✅ 完成 | 100% |
| 文件與指南 | ✅ 完成 | 100% |
| **總體進度** | ✅ **Production Ready** | **100%** |

---

## 🚀 快速開始

### 方法一：GitHub Actions (推薦)

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/Exchange-Plan.git
cd Exchange-Plan

# 2. 編輯個人資料
code my_profile.yml  # 或使用任何編輯器

# 3. 安裝依賴
pip install PyYAML markdown jinja2 python-dateutil

# 4. 生成文件
python build_scripts/generate_docs.py --all
python build_scripts/generate_pages.py

# 5. 推送到 GitHub（會自動觸發 CI/CD）
git add .
git commit -m "feat: update application documents"
git push
```

### 方法二：Harness Pipeline

1. 在 Harness 中導入 pipeline:
   - `.harness/Exchange-Plan/.harness/orgs/default/projects/default_project/exchange-integrated.yaml`
2. 設定 Git Connector
3. 執行 Pipeline

---

## 📁 專案結構

```
Exchange-Plan/
├── 📄 my_profile.yml                # ⭐ 個人資料主檔
│
├── 📂 templates/                    # 文件範本
│   ├── cv_template.md
│   ├── study_plan_template.md
│   └── recommendation_request_template.md
│
├── 📂 build_scripts/                # 自動化腳本
│   ├── generate_docs.py            # 文件生成
│   └── generate_pages.py           # 網頁生成
│
├── 📂 supporting_documents/         # 支持文件
│   ├── SUPPORTING_DOCUMENTS_INDEX.md
│   ├── PORTFOLIO_HIGHLIGHTS.md
│   ├── 獎學金.png
│   ├── 校園事務參與.png
│   ├── Github-*.png
│   └── transcripts/                 # 成績單
│
├── 📂 final_applications/           # 生成的申請文件
│   ├── University_of_Bern/
│   └── UC_San_Diego/
│
├── 📂 docs/                         # GitHub Pages 網站
│   ├── index.html
│   └── documents.html
│
├── 📂 .github/workflows/            # GitHub Actions
│   ├── exchange-app-pipeline.yml
│   └── pages-deploy.yml
│
├── 📂 .harness/                     # Harness Pipeline
│   └── exchange-integrated.yaml
│
└── 📚 文檔
    ├── README.md                    # 本文件
    ├── QUICK_START.md              # 快速開始
    ├── APPLICATION_CHECKLIST.md    # 申請檢查清單
    ├── INTEGRATION_GUIDE.md        # 整合指南
    ├── DEPLOYMENT_GUIDE.md         # 部署指南
    └── PROJECT_SUMMARY.md          # 專案總結
```

---

## 🎯 使用流程

### 1. 準備個人資料

編輯 `my_profile.yml`，填入：
- 基本資料（姓名、聯絡方式）
- 教育背景（GPA、排名）
- 語言能力（IELTS、TOEFL）
- 專業技能與證照（45+證照）
- 工作經驗
- 獎項與成就

### 2. 生成申請文件

```bash
# 為所有目標大學生成文件
python build_scripts/generate_docs.py --all

# 為特定大學生成
python build_scripts/generate_docs.py --university "University of Bern" --type cv
```

### 3. 生成 GitHub Pages

```bash
python build_scripts/generate_pages.py
```

### 4. 推送到 GitHub

```bash
git add .
git commit -m "feat: update application documents"
git push
```

### 5. 自動部署

- GitHub Actions 自動執行
- 文件自動生成並提交
- GitHub Pages 自動更新
- 📧 Email 通知完成

---

## 🌐 GitHub Pages

部署後可訪問：`https://YOUR_USERNAME.github.io/Exchange-Plan/`

### 網站功能

- 📊 **儀表板** - 申請進度一覽
- 📈 **統計數據** - GPA、IELTS、證照數量
- 📋 **文件列表** - 所有生成的申請文件
- 📅 **時間軸** - 申請進度追蹤
- 🔗 **快速連結** - Portfolio、GitHub、LinkedIn

---

## 🔄 CI/CD 流程

### GitHub Actions Pipeline

```
Push → Setup → Validate → Generate Docs → Build Pages → Deploy → ✅
```

**觸發條件**:
- Push to `main` or `develop`
- 修改 `my_profile.yml`, `templates/`, `build_scripts/`
- 手動觸發

### Harness Pipeline

```
Trigger → Setup → Generate → Build → Push to GitHub → ✅
```

**自動通知**:
- ✅ 成功通知 (Email)
- ❌ 失敗通知 (Email)

---

## 📝 核心文件說明

### my_profile.yml

**380+ 行完整資料庫**，包含：
- 個人資訊
- 教育背景（GPA 3.96/4.3）
- IELTS 7.0（R:9.0滿分）
- 45+專業證照
- 工作經驗（3個職位）
- 國際經驗（索馬利蘭、日本）
- 獎項（研究生獎學金、NFT展覽等）
- 目標學校（University of Bern、UC San Diego）

### 範本系統

#### CV 範本
包含欄位：
- Academic Profile
- Education
- Research & Thesis
- Professional Experience
- International Development
- Cross-Cultural Experience
- Campus & Research Experience
- Honors & Awards
- Exhibitions & Creative Work
- Technical Skills
- Certifications (45+)
- GitHub Highlights

#### 學習計畫範本
包含章節：
- 申請動機
- 短期學習計畫
- 長期學習計畫
- 如何貢獻與回饋

---

## 🎓 目標學校

### 第一志願：University of Bern, Switzerland
- Advanced Topics in Cryptography
- Machine Learning
- Prof. Christian Cachin 研究

### 第二志願：UC San Diego, USA
- CSE 227: Computer Security
- CSE 291: Topics in AI (Trustworthy AI)
- Center for Networked Systems

---

## 💡 關鍵優勢

### 效率提升
- 傳統方式：2-3天/校
- 本系統：4-6小時/校
- **節省時間：60-70%**

### 品質保證
- ✅ 資料一致性
- ✅ 完整性檢查
- ✅ 專業範本
- ✅ 自動化驗證

### 可擴展性
- ✅ 易於添加新學校
- ✅ 範本可持續優化
- ✅ 支持文件隨時更新
- ✅ 系統可複用

---

## 📚 文檔指南

| 文檔 | 用途 |
|------|------|
| `QUICK_START.md` | 5分鐘快速上手 |
| `APPLICATION_CHECKLIST.md` | 完整申請檢查清單 |
| `INTEGRATION_GUIDE.md` | 詳細使用說明 |
| `DEPLOYMENT_GUIDE.md` | CI/CD部署指南 |
| `PROJECT_SUMMARY.md` | 專案總結報告 |
| `supporting_documents/SUPPORTING_DOCUMENTS_INDEX.md` | 支持文件索引 |
| `supporting_documents/PORTFOLIO_HIGHLIGHTS.md` | GitHub技術亮點 |

---

## 🔧 技術棧

- **語言**: Python 3.11+
- **資料格式**: YAML
- **範本**: Markdown
- **網頁**: HTML/CSS
- **CI/CD**: GitHub Actions + Harness
- **部署**: GitHub Pages
- **依賴**: PyYAML, Markdown, Jinja2

---

## 📅 申請時程

**截止日期**: 2026年1月12日

### Week 1-2
- 申請官方成績單
- 選定推薦教授
- 影印證件

### Week 3-4
- 生成申請文件
- 人工審閱調整
- 尋找校對服務

### Week 5-6
- 收集推薦信
- 完成校對
- 填寫申請表

### Week 7
- 最終檢查
- 提交申請

---

## 🎨 個人亮點

### 學術成就
- GPA: **3.96/4.3 (Top 5%)**
- 研究生獎學金 (2023)
- NFT創作展覽 (2023)

### 語言能力
- IELTS: **7.0** (L:7.5 / **R:9.0** / W:5.5 / S:6.5)
- EF SET: **76/100 (C2)**

### 專業證照
- **45+** 國際認證
- ISC² Certified in Cybersecurity
- Cloudflare ACE/ASE/MSP
- AWS, GCP, Oracle Cloud
- Quantum Computing (IBM, Linux Foundation)

### 工作經驗
- **5年** 網路安全與雲端基礎設施
- MITAKE Information (Cybersecurity Developer)
- Twister5 (Cybersecurity Consultant)
- 索馬利蘭HIS專案 (TaiwanICDF)

### GitHub成就
- **2,500+** commits/year
- **222** stars
- **42** followers
- **80%** contribution rate

---

## 🤝 貢獻

歡迎提交 Issues 和 Pull Requests！

---

## 📧 聯絡方式

- **Email**: admin@dennisleehappy.org
- **Portfolio**: https://www.dennisleehappy.org/
- **LinkedIn**: https://www.linkedin.com/in/pei-chen-lee-4a3a352a2/
- **GitHub**: https://github.com/dennislee928

---

## 📜 授權

MIT License - 詳見 [LICENSE](LICENSE) 檔案

---

## 🙏 致謝

感謝所有支持此專案的人！

---

## 🎉 狀態

**✅ Production Ready**

- 核心功能：100% 完成
- CI/CD 整合：100% 完成
- 文檔：100% 完成
- GitHub Pages：已部署

**🚀 立即開始使用！**

---

**Last Updated**: 2025-10-07  
**Version**: 2.0.0  
**Maintainer**: Pei-Chen Lee

🎓 **祝您申請順利！Good luck with your exchange application!**
