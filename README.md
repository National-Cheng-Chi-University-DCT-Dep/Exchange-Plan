專案目標：「交換申請情報與自動化中心 (ExchangeApp-IAC)」
一個基於 CI/CD 的自動化平台，旨在將校內交換申請流程從手動追蹤，轉變為一個數據驅動、可監控、具備內部競爭策略輔助能力的工程專案。

第一階段 (Phase 1): 核心情報與文件客製化
目標：建立一個能集中管理校級與院級交換機會、驗證資格、並快速生成客製化申請文件的基礎工作流。

TODO-1: 建立「交換專用」Repo 結構

[ ] 初始化 GitHub Repo (NCCU-Exchange-IAC)。

[ ] 建立核心目錄結構：

/.harness/ (Harness Pipeline 設定)

/source_data/ (存放交換機會的原始資料)

university_level_options.yml (校級交換機會清單)

college_level_options.yml (院級交換機會清單)

my_profile.yml (存放您的個人條件，如碩士GPA、雅思成績、已修課程)

/intelligence_gathering/ (取代 data_collection，更強調情報分析)

validator.py (資格驗證腳本)

course_matcher.py (姊妹校課程比對腳本)

/templates/

study_plan_template.md (讀書計畫通用範本)

cv_template.md (履歷範本)

/final_applications/ (存放為每個學校客製化的最終文件)

/build_scripts/ (文件生成腳本)

TODO-2: 手動建立核心資料庫 (Manual Database Setup)

[ ] 廢除通用爬蟲，改為手動精準填寫。

[ ] 在 university_level_options.yml 和 college_level_options.yml 中，根據 OIC 和傳播學院的簡章，手動建立資料結構，包含：

school_name, country, internal_deadline, ielts_requirement, slots_available, official_info_url, notable_courses 等欄位。

TODO-3: 實作資格驗證與課程匹配模組

[ ] 在 /intelligence_gathering/validator.py 中：

核心功能：讀取 my_profile.yml 和所有 options.yml，自動比對您的碩士 GPA 和雅思成績是否符合每個交換機會的內部申請門檻。

產出：生成一份 /final_applications/eligibility_report.md，清晰標示出您符合哪些學校的申請資格。

[ ] 在 /intelligence_gathering/course_matcher.py 中：

進階功能：手動在 options.yml 的 notable_courses 欄位中填入幾門您感興趣的姊妹校課程。此腳本會比對 my_profile.yml 中您已修過的政大課程，找出可能的關聯性，為您的讀書計畫提供論述基礎。

TODO-4: 建立文件生成與 CI/CD Pipeline

[ ] 在 build_scripts/generate_docs.py 中，建立一個能根據不同學校 options.yml 中的關鍵字，客製化 study_plan_template.md 的腳本。

[ ] 在 /.harness/ 中建立 exchange_pipeline.yml。

Pipeline 流程：

觸發 (Trigger)：手動觸發，或當 options.yml 更新時觸發。

階段 1 (Validate)：運行 validator.py，生成資格報告。

階段 2 (Generate)：運行 generate_docs.py，為所有符合資格的學校，生成初步的客製化讀書計畫草稿。

產物儲存：將所有草稿文件存放在 /final_applications/。

第二階段 (Phase 2): 打造交換申請指揮中心
目標：建立一個能鳥瞰全局、追蹤進度、並自動提醒的儀表板。

TODO-5: 建立交換申請儀表板 (Dashboard)

[ ] 在所有 options.yml 檔案中增加 application_status 欄位 (Not Started, Drafting, Submitted, Interviewing, Nominated)。

[ ] 修改 generate_docs.py，使其每次運行都更新一份 dashboard.md。

儀表板內容：

校級/院級申請總覽：一個表格，包含學校名稱、國家、內部申請截止日期、狀態。

個人準備進度：Checklist，包含「英語檢定」、「成績單申請」、「自傳」、「讀書計畫」、「推薦信」等。

資格符合性速覽：直接嵌入 eligibility_report.md 的內容。

TODO-6: 整合智慧化任務管理

[ ] 修改 validator.py，當偵測到一個交換機會的 internal_deadline 在兩週內時，自動調用 GitHub API 創建一個標題為 [URGENT] Submit application for [School Name] 的 Issue，並 assign 給您自己。

第三階段 (Phase 3): 升級為交換策略中心
目標：引入分析工具，從「管理」申請進化到「策略性贏得」申請。

TODO-7: 實作「內部競爭」預測性分析

[ ] 競爭激烈度模型：

在 options.yml 中增加一個 predicted_competition_score (1-10) 的欄位。

建立一個 scoring_engine.py，根據啟發式規則為每個機會打分。規則可包含：

國家熱門度 (例如：美國/英國/德國 +3分)

名額稀有度 (1個名額 +2分，3個名額 +0分)

語言門檻 (僅要求B2 +1分，因為競爭者更多)

在儀表板上視覺化這個分數，幫助您判斷哪些是熱門選項，哪些是藍海機會。

TODO-8: 開發進階情報模組

[ ] 學分抵免雷達 (Credit Transfer Radar)：

擴充 course_matcher.py，使其能（在您手動提供課程大綱後）初步分析姊妹校課程與政大課程的相似度，生成一份「學分抵免可能性報告」，讓您的讀書計畫更有說服力。

[ ] 學長姐經驗分析儀 (Alumni Experience Analyzer)：

建立一個手動的情報資料夾 /intelligence_gathering/alumni_notes/。

在 Dcard、PTT 等論壇搜尋政大學長姐分享的特定姊妹校交換心得，將重點（如推薦的課、遇到的坑）整理成 Markdown 筆記，方便查閱。

TODO-9: 引入「遊戲化」激勵引擎

[ ] 成就與徽章系統：

OIC Explorer (完成校級交換資料庫建立)

College Insider (完成院級交換資料庫建立)

First Move (提交第一份校內申請)

Nomination Secured! (獲得第一個交換推薦資格)

[ ] 進度條視覺化：在 dashboard.md 中，建立一個基於您 application_status 欄位的總進度條，讓您看見從 Not Started 到 Nominated 的每一步進展。
