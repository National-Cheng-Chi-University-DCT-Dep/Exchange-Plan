#!/usr/bin/env python3
"""
交換申請資格驗證腳本
讀取 my_profile.yml 和所有 options.yml，自動比對申請資格
"""

import yaml
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any

class ExchangeValidator:
    def __init__(self, profile_path: str = "my_profile.yml"):
        """初始化驗證器"""
        self.profile_path = profile_path
        self.profile_data = self._load_yaml(profile_path)
        self.university_options = self._load_yaml("source_data/university_level_options.yml")
        self.college_options = self._load_yaml("source_data/college_level_options.yml")
        
    def _load_yaml(self, file_path: str) -> Dict[str, Any]:
        """載入YAML檔案"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"警告: 找不到檔案 {file_path}")
            return {}
        except yaml.YAMLError as e:
            print(f"錯誤: 解析YAML檔案 {file_path} 時發生錯誤: {e}")
            return {}
    
    def check_language_requirements(self, university: Dict[str, Any]) -> Dict[str, Any]:
        """檢查語言要求"""
        result = {
            "meets_ielts": False,
            "meets_toefl": False,
            "meets_other": False,
            "missing_requirements": [],
            "score_details": {}
        }
        
        profile_lang = self.profile_data.get("language_proficiency", {}).get("english", {})
        
        # 檢查IELTS要求
        if "ielts_requirement" in university:
            ielts_req = university["ielts_requirement"]
            ielts_score = profile_lang.get("ielts", {}).get("overall_score")
            
            if ielts_score is not None:
                result["score_details"]["ielts"] = {
                    "required": ielts_req,
                    "current": ielts_score,
                    "meets": ielts_score >= ielts_req
                }
                result["meets_ielts"] = ielts_score >= ielts_req
            else:
                result["missing_requirements"].append(f"IELTS成績 (需要 {ielts_req})")
        
        # 檢查TOEFL要求
        if "toefl_requirement" in university:
            toefl_req = university["toefl_requirement"]
            toefl_score = profile_lang.get("toefl", {}).get("total_score")
            
            if toefl_score is not None:
                result["score_details"]["toefl"] = {
                    "required": toefl_req,
                    "current": toefl_score,
                    "meets": toefl_score >= toefl_req
                }
                result["meets_toefl"] = toefl_score >= toefl_req
            else:
                result["missing_requirements"].append(f"TOEFL成績 (需要 {toefl_req})")
        
        # 檢查其他語言要求
        if "german_requirement" in university:
            german_req = university["german_requirement"]
            result["missing_requirements"].append(f"德語能力證明 (需要 {german_req})")
            result["meets_other"] = False
        
        return result
    
    def check_academic_requirements(self, university: Dict[str, Any]) -> Dict[str, Any]:
        """檢查學術要求"""
        result = {
            "meets_gpa": False,
            "gpa_details": {},
            "missing_requirements": []
        }
        
        # 獲取當前GPA
        current_gpa = self.profile_data.get("education", {}).get("current_program", {}).get("gpa")
        max_gpa = self.profile_data.get("education", {}).get("current_program", {}).get("max_gpa")
        
        if current_gpa is not None and max_gpa is not None:
            gpa_percentage = (current_gpa / max_gpa) * 100
            
            # 假設大部分學校要求GPA在3.0/4.0以上或80%以上
            # 實際要求可能需要根據具體學校調整
            meets_gpa = gpa_percentage >= 80  # 80%相當於3.2/4.0
            
            result["gpa_details"] = {
                "current_gpa": current_gpa,
                "max_gpa": max_gpa,
                "percentage": gpa_percentage,
                "meets_standard": meets_gpa
            }
            result["meets_gpa"] = meets_gpa
        else:
            result["missing_requirements"].append("GPA成績")
        
        return result
    
    def check_deadline_status(self, university: Dict[str, Any]) -> Dict[str, Any]:
        """檢查申請截止日期狀態"""
        result = {
            "deadline_status": "unknown",
            "days_remaining": None,
            "is_urgent": False,
            "deadline_date": None
        }
        
        deadline_str = university.get("internal_deadline")
        if deadline_str:
            try:
                deadline_date = datetime.strptime(deadline_str, "%Y-%m-%d")
                today = datetime.now()
                days_remaining = (deadline_date - today).days
                
                result["deadline_date"] = deadline_str
                result["days_remaining"] = days_remaining
                
                if days_remaining < 0:
                    result["deadline_status"] = "expired"
                elif days_remaining <= 7:
                    result["deadline_status"] = "urgent"
                    result["is_urgent"] = True
                elif days_remaining <= 30:
                    result["deadline_status"] = "soon"
                else:
                    result["deadline_status"] = "ok"
                    
            except ValueError:
                result["deadline_status"] = "invalid_date"
        
        return result
    
    def validate_university(self, university: Dict[str, Any]) -> Dict[str, Any]:
        """驗證單一學校的申請資格"""
        school_name = university.get("school_name", "Unknown")
        
        # 執行各項檢查
        language_check = self.check_language_requirements(university)
        academic_check = self.check_academic_requirements(university)
        deadline_check = self.check_deadline_status(university)
        
        # 計算整體資格符合度
        meets_requirements = (
            (language_check["meets_ielts"] or language_check["meets_toefl"]) and
            academic_check["meets_gpa"] and
            deadline_check["deadline_status"] not in ["expired", "invalid_date"]
        )
        
        # 計算競爭分數影響
        competition_score = university.get("predicted_competition_score", 5)
        slots_available = university.get("slots_available", 1)
        
        # 根據資格和競爭情況給出建議
        recommendation = self._generate_recommendation(
            meets_requirements, competition_score, slots_available, deadline_check["is_urgent"]
        )
        
        return {
            "school_name": school_name,
            "country": university.get("country", "Unknown"),
            "meets_requirements": meets_requirements,
            "language_check": language_check,
            "academic_check": academic_check,
            "deadline_check": deadline_check,
            "competition_score": competition_score,
            "slots_available": slots_available,
            "recommendation": recommendation,
            "application_status": university.get("application_status", "Not Started")
        }
    
    def _generate_recommendation(self, meets_requirements: bool, competition_score: int, 
                               slots_available: int, is_urgent: bool) -> str:
        """生成申請建議"""
        if not meets_requirements:
            return "不符合基本要求，不建議申請"
        
        if is_urgent:
            return "⚠️ 緊急：截止日期即將到期，建議立即準備申請文件"
        
        if competition_score >= 8 and slots_available <= 1:
            return "🔥 高競爭：競爭激烈且名額稀少，需要準備最強申請文件"
        elif competition_score >= 6:
            return "⚡ 中等競爭：有一定競爭，建議認真準備申請文件"
        else:
            return "✅ 低競爭：競爭較小，申請成功機會較高"
    
    def validate_all_universities(self) -> List[Dict[str, Any]]:
        """驗證所有大學的申請資格"""
        results = []
        
        # 驗證校級交換機會
        universities = self.university_options.get("universities", [])
        for university in universities:
            result = self.validate_university(university)
            result["program_type"] = "University Level"
            results.append(result)
        
        # 驗證院級交換機會
        colleges = self.college_options.get("universities", [])
        for college in colleges:
            result = self.validate_university(college)
            result["program_type"] = "College Level"
            results.append(result)
        
        return results
    
    def generate_eligibility_report(self, output_path: str = "final_applications/eligibility_report.md"):
        """生成資格報告"""
        results = self.validate_all_universities()
        
        # 按資格符合度和競爭分數排序
        eligible_results = [r for r in results if r["meets_requirements"]]
        eligible_results.sort(key=lambda x: (x["competition_score"], x["deadline_check"]["days_remaining"] or 999))
        
        # 生成報告內容
        report_content = self._format_eligibility_report(eligible_results, results)
        
        # 確保輸出目錄存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 寫入報告
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(report_content)
        
        print(f"資格報告已生成: {output_path}")
        return output_path
    
    def _format_eligibility_report(self, eligible_results: List[Dict], all_results: List[Dict]) -> str:
        """格式化資格報告內容"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""# 交換申請資格報告
*生成時間: {current_time}*

## 📊 總覽

- **總計學校數**: {len(all_results)}
- **符合資格學校數**: {len(eligible_results)}
- **資格符合率**: {len(eligible_results)/len(all_results)*100:.1f}%

## ✅ 符合申請資格的學校

"""
        
        if not eligible_results:
            report += "❌ 目前沒有符合申請資格的學校，請檢查語言成績要求。\n\n"
        else:
            for i, result in enumerate(eligible_results, 1):
                report += f"""### {i}. {result['school_name']} ({result['country']})

- **計畫類型**: {result['program_type']}
- **競爭分數**: {result['competition_score']}/10
- **名額**: {result['slots_available']}個
- **申請狀態**: {result['application_status']}
- **建議**: {result['recommendation']}

**截止日期狀態**:
"""
                deadline_info = result['deadline_check']
                if deadline_info['days_remaining'] is not None:
                    if deadline_info['days_remaining'] > 0:
                        report += f"- 📅 剩餘 {deadline_info['days_remaining']} 天\n"
                    else:
                        report += f"- ❌ 已過期 {abs(deadline_info['days_remaining'])} 天\n"
                else:
                    report += "- ❓ 日期資訊不明\n"
                
                report += f"- 📊 狀態: {deadline_info['deadline_status']}\n\n"
        
        # 添加不符合資格的學校
        ineligible_results = [r for r in all_results if not r["meets_requirements"]]
        if ineligible_results:
            report += """## ❌ 不符合申請資格的學校

"""
            for result in ineligible_results:
                report += f"""### {result['school_name']} ({result['country']})
- **計畫類型**: {result['program_type']}
- **不符合原因**:
"""
                # 添加具體的不符合原因
                if not result['language_check']['meets_ielts'] and not result['language_check']['meets_toefl']:
                    report += "  - 語言成績不符合要求\n"
                if not result['academic_check']['meets_gpa']:
                    report += "  - 學術成績不符合要求\n"
                if result['deadline_check']['deadline_status'] in ['expired', 'invalid_date']:
                    report += "  - 申請截止日期已過期或無效\n"
                
                report += "\n"
        
        report += """## 📋 建議行動

### 立即行動項目
"""
        
        # 檢查緊急申請
        urgent_applications = [r for r in eligible_results if r['deadline_check']['is_urgent']]
        if urgent_applications:
            report += "- 🚨 **緊急**: 以下學校申請截止日期即將到期:\n"
            for app in urgent_applications:
                report += f"  - {app['school_name']} (剩餘 {app['deadline_check']['days_remaining']} 天)\n"
            report += "\n"
        
        report += """### 準備項目
- 完成英語檢定考試 (IELTS/TOEFL)
- 準備推薦信
- 撰寫讀書計畫
- 整理成績單和證照

### 申請策略建議
- 優先申請競爭較低且有充足時間準備的學校
- 對於高競爭學校，需要準備最強申請文件
- 建議申請3-5所學校，包含不同競爭程度的選項

---
*此報告由 ExchangeApp-IAC 自動生成*
"""
        
        return report

def main():
    """主函數"""
    print("開始交換申請資格驗證...")
    
    # 檢查必要檔案是否存在
    required_files = ["my_profile.yml", "source_data/university_level_options.yml", "source_data/college_level_options.yml"]
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"缺少必要檔案: {', '.join(missing_files)}")
        return
    
    # 執行驗證
    validator = ExchangeValidator()
    report_path = validator.generate_eligibility_report()
    
    print("資格驗證完成!")
    print(f"報告位置: {report_path}")

if __name__ == "__main__":
    main()
