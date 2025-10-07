# ExchangeApp-IAC 使用指南

## 🚀 快速開始

### 1. 環境準備
```bash
# 確保已安裝Python 3.7+
python3 --version

# 安裝必要套件
pip3 install pyyaml
```

### 2. 更新個人資料
編輯 `my_profile.yml` 檔案，更新您的個人條件：
- 學術成績 (GPA)
- 語言能力 (IELTS/TOEFL成績)
- 已修課程
- 工作經驗
- 證照資訊

### 3. 更新交換機會資料
編輯以下檔案以更新可申請的學校：
- `source_data/university_level_options.yml` - 校級交換機會
- `source_data/college_level_options.yml` - 院級交換機會

### 4. 執行資格驗證
```bash
python3 intelligence_gathering/validator.py
```
這會生成 `final_applications/eligibility_report.md` 報告。

### 5. 生成申請文件
```bash
python3 build_scripts/generate_docs.py
```
這會為每個學校生成客製化的：
- 讀書計畫 (study_plan)
- 履歷 (CV)
- 申請進度儀表板 (dashboard.md)

## 📁 檔案結構

```
Exchange-Plan/
├── my_profile.yml                    # 個人條件檔案
├── source_data/                      # 交換機會資料
│   ├── university_level_options.yml  # 校級交換機會
│   └── college_level_options.yml     # 院級交換機會
├── intelligence_gathering/           # 資格驗證模組
│   └── validator.py                  # 資格驗證腳本
├── templates/                        # 文件範本
│   ├── study_plan_template.md        # 讀書計畫範本
│   └── cv_template.md               # 履歷範本
├── build_scripts/                    # 文件生成腳本
│   └── generate_docs.py             # 文件生成器
├── final_applications/               # 生成的申請文件
│   ├── eligibility_report.md         # 資格報告
│   ├── dashboard.md                  # 申請進度儀表板
│   └── [學校名稱]/                   # 各校申請文件
└── .harness/                         # CI/CD配置
    └── exchange_pipeline.yml         # Harness Pipeline配置
```

## 🔧 主要功能

### 資格驗證 (validator.py)
- 自動檢查語言成績要求 (IELTS/TOEFL)
- 驗證學術成績 (GPA)
- 檢查申請截止日期
- 評估競爭激烈度
- 生成資格報告

### 文件生成 (generate_docs.py)
- 根據學校特色客製化讀書計畫
- 調整履歷重點
- 自動替換範本變數
- 生成申請進度儀表板

### 範本客製化
- 讀書計畫會根據學校特色調整專業領域
- 履歷會強調相關的工作經驗
- 自動建議適合的課程和教授

## 📊 使用範例

### 1. 檢查申請資格
```bash
python3 intelligence_gathering/validator.py
```

輸出範例：
```
🔄 開始交換申請資格驗證...
✅ 資格驗證完成!
📄 報告位置: final_applications/eligibility_report.md
```

### 2. 生成申請文件
```bash
python3 build_scripts/generate_docs.py
```

輸出範例：
```
🔄 開始生成申請文件...
✅ 已生成 University of California, Berkeley 的申請文件
✅ 已生成 Massachusetts Institute of Technology 的申請文件
✅ 已生成 Tallinn University of Technology (TalTech) 的申請文件
✅ 文件生成完成!
📊 儀表板位置: final_applications/dashboard.md
📁 共生成 8 所學校的申請文件
```

## 🎯 下一步行動

1. **檢查生成的文件**
   - 查看 `final_applications/dashboard.md` 了解申請進度
   - 檢查各校的讀書計畫和履歷是否符合要求

2. **準備缺失的文件**
   - 英語檢定成績 (IELTS/TOEFL)
   - 推薦信
   - 成績單申請

3. **根據各校要求調整**
   - 手動調整讀書計畫的特定內容
   - 根據學校特色強調相關經驗

4. **提交申請**
   - 注意各校申請截止日期
   - 準備線上申請系統所需資料

## ⚠️ 注意事項

- 請定期更新 `my_profile.yml` 中的最新資訊
- 英語檢定成績欄位目前為空，需要填入實際成績
- 生成的範本是基礎版本，建議根據各校要求進行調整
- 申請截止日期請以學校官方公告為準

## 🆘 常見問題

### Q: 如何更新學校清單？
A: 編輯 `source_data/` 目錄下的 YAML 檔案，按照現有格式添加新的學校資訊。

### Q: 生成的讀書計畫太通用怎麼辦？
A: 這是正常的，系統生成的範本需要根據各校特色手動調整。可以參考範本中的 `[變數]` 標記進行客製化。

### Q: 如何添加新的文件範本？
A: 在 `templates/` 目錄下添加新的範本檔案，然後在 `generate_docs.py` 中添加對應的處理邏輯。

---

*此使用指南會隨著系統功能更新而持續改進*
