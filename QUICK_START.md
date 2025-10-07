# Quick Start Guide
## 快速開始使用 Exchange-Plan 系統

**目標**: 5分鐘內了解如何使用本系統生成申請文件

---

## 🚀 三步驟開始

### Step 1: 生成申請文件 (2分鐘)

打開PowerShell或命令提示字元：

```bash
# 切換到專案目錄
cd C:\Users\pclee\Documents\GitHub\Exchange-Plan

# 安裝依賴（僅首次需要）
pip install pyyaml

# 生成所有申請文件
python build_scripts/generate_docs.py --all
```

**結果**: 在 `final_applications/` 目錄下會生成：
- `University_of_Bern/University_of_Bern_cv_YYYYMMDD.md`
- `University_of_Bern/University_of_Bern_study_plan_YYYYMMDD.md`
- `UC_San_Diego/UC_San_Diego_cv_YYYYMMDD.md`
- `UC_San_Diego/UC_San_Diego_study_plan_YYYYMMDD.md`

---

### Step 2: 審閱並調整內容 (30-60分鐘)

1. 開啟生成的文件
2. 尋找 `[TO BE FILLED]` 標記
3. 填入具體資訊
4. 調整語氣和用詞
5. 確保內容連貫

**建議**: 使用 VS Code 或任何Markdown編輯器

---

### Step 3: 準備支持文件 (30分鐘)

參考 `supporting_documents/SUPPORTING_DOCUMENTS_INDEX.md`：

1. 開啟索引文件
2. 按照順序檢查每份文件
3. 轉換為PDF格式
4. 準備提交包

---

## 📋 完整申請流程

### Week 1-2: 準備官方文件
- [ ] 向教務處申請英文成績單
- [ ] 選定推薦教授
- [ ] 影印身分證、學生證、護照

### Week 3-4: 完成申請文件
- [ ] 執行 `generate_docs.py`
- [ ] 人工調整內容
- [ ] 尋找英文校對服務
- [ ] 準備推薦信資料包

### Week 5-6: 收集材料
- [ ] 寄送推薦信請求
- [ ] 完成英文校對
- [ ] 填寫申請表
- [ ] 整理支持文件

### Week 7: 提交申請
- [ ] 最終檢查（使用 APPLICATION_CHECKLIST.md）
- [ ] 轉換所有文件為PDF
- [ ] 提交申請（2026年1月12日前）

---

## 📁 重要文件快速索引

| 文件 | 路徑 | 用途 |
|------|------|------|
| 個人資料 | `my_profile.yml` | 所有資訊的來源 |
| 申請檢查清單 | `APPLICATION_CHECKLIST.md` | 逐項檢查 |
| 整合指南 | `INTEGRATION_GUIDE.md` | 詳細使用說明 |
| 支持文件索引 | `supporting_documents/SUPPORTING_DOCUMENTS_INDEX.md` | 文件清單 |
| Portfolio亮點 | `supporting_documents/PORTFOLIO_HIGHLIGHTS.md` | GitHub成就 |
| 生成腳本 | `build_scripts/generate_docs.py` | 自動化工具 |

---

## 💡 常見問題

### Q1: 如何修改個人資訊？
**A**: 編輯 `my_profile.yml`，然後重新執行生成腳本

### Q2: 如何為新學校生成文件？
**A**: 
```bash
python build_scripts/generate_docs.py --university "School Name" --type both
```

### Q3: 生成的文件還需要什麼調整？
**A**: 
1. 填補 `[TO BE FILLED]` 標記
2. 調整為具體案例（不要太通用）
3. 確保語氣一致
4. 英文校對

### Q4: 支持文件如何準備？
**A**: 參考 `supporting_documents/SUPPORTING_DOCUMENTS_INDEX.md`，按順序整理成PDF

---

## ⚡ 快速命令參考

```bash
# 只生成CV
python build_scripts/generate_docs.py --university "University of Bern" --type cv

# 只生成學習計畫
python build_scripts/generate_docs.py --university "UC San Diego" --type study_plan

# 生成所有文件
python build_scripts/generate_docs.py --all

# 查看個人資料
cat my_profile.yml

# 查看目錄結構
tree /F
```

---

## 🎯 今天就可以做的事

1. ✅ 執行文件生成腳本測試
2. ✅ 查閱生成的CV和學習計畫
3. ✅ 開始申請英文成績單
4. ✅ 思考推薦教授人選
5. ✅ 閱讀 APPLICATION_CHECKLIST.md

---

## 📞 需要幫助？

參考以下文件獲得詳細說明：
- **使用問題**: `INTEGRATION_GUIDE.md`
- **申請流程**: `APPLICATION_CHECKLIST.md`
- **專案總覽**: `PROJECT_SUMMARY.md`
- **支持文件**: `supporting_documents/SUPPORTING_DOCUMENTS_INDEX.md`

---

**開始時間**: 現在  
**預計完成**: 6-7週後  
**申請截止**: 2026年1月12日

**Good luck with your exchange application! 🎓**

