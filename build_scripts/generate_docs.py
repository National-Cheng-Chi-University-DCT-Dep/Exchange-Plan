#!/usr/bin/env python3
"""
文件生成腳本
根據不同學校的options.yml，客製化生成申請文件
"""

import yaml
import os
import re
from datetime import datetime
from typing import Dict, List, Any

class DocumentGenerator:
    def __init__(self, profile_path: str = "my_profile.yml"):
        """初始化文件生成器"""
        self.profile_path = profile_path
        self.profile_data = self._load_yaml(profile_path)
        self.template_dir = "templates"
        self.output_dir = "final_applications"
        
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
    
    def _load_template(self, template_name: str) -> str:
        """載入範本檔案"""
        template_path = os.path.join(self.template_dir, template_name)
        try:
            with open(template_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"警告: 找不到範本檔案 {template_path}")
            return ""
    
    def _replace_template_variables(self, template: str, variables: Dict[str, str]) -> str:
        """替換範本中的變數"""
        for key, value in variables.items():
            placeholder = f"[{key}]"
            template = template.replace(placeholder, str(value))
        return template
    
    def _extract_course_info(self, university: Dict[str, Any]) -> str:
        """提取課程資訊"""
        notable_courses = university.get("notable_courses", [])
        if not notable_courses:
            return "Advanced Computer Science courses, Cybersecurity, Machine Learning"
        
        # 格式化課程列表
        course_list = []
        for course in notable_courses[:3]:  # 只取前3門課程
            course_list.append(f"- {course}")
        
        return "\n".join(course_list)
    
    def _get_specialized_area(self, university: Dict[str, Any]) -> str:
        """根據學校特色決定專業領域"""
        country = university.get("country", "").lower()
        school_name = university.get("school_name", "").lower()
        
        if "cybersecurity" in school_name or "security" in school_name:
            return "Cybersecurity"
        elif "quantum" in school_name:
            return "Quantum Computing"
        elif country in ["germany", "netherlands"]:
            return "Advanced Computer Security"
        elif country in ["united states", "united kingdom"]:
            return "AI-driven Security Systems"
        else:
            return "Computer Science"
    
    def _get_target_courses(self, university: Dict[str, Any]) -> str:
        """獲取目標課程"""
        notable_courses = university.get("notable_courses", [])
        if notable_courses:
            return ", ".join(notable_courses[:2])  # 取前2門課程
        else:
            return "Advanced Computer Security, Machine Learning, Quantum Computing"
    
    def _get_professor_suggestions(self, university: Dict[str, Any]) -> str:
        """根據學校建議適合的教授"""
        school_name = university.get("school_name", "").lower()
        country = university.get("country", "").lower()
        
        if "taltech" in school_name:
            return "Prof. Rain Ottis (Cybersecurity), Prof. Samuel Pagliarini (Hardware Security), Prof. Ahto Buldas (Cryptography)"
        elif "mit" in school_name:
            return "Prof. Ronald Rivest (Cryptography), Prof. Nancy Lynch (Distributed Systems)"
        elif "stanford" in school_name:
            return "Prof. Dan Boneh (Cryptography), Prof. Monica Lam (Computer Security)"
        elif "cambridge" in school_name:
            return "Prof. Ross Anderson (Security Engineering), Prof. Frank Stajano (Security)"
        elif country == "germany":
            return "Cybersecurity and Quantum Computing research faculty"
        else:
            return "Computer Science and Cybersecurity faculty"
    
    def generate_study_plan(self, university: Dict[str, Any]) -> str:
        """生成客製化讀書計畫"""
        template = self._load_template("study_plan_template.md")
        if not template:
            return ""
        
        # 準備變數
        school_name = university.get("school_name", "Unknown University")
        country = university.get("country", "Unknown Country")
        specialized_area = self._get_specialized_area(university)
        target_courses = self._get_target_courses(university)
        course_info = self._extract_course_info(university)
        professor_suggestions = self._get_professor_suggestions(university)
        
        # 根據學校特色調整專業領域描述
        if country == "Estonia":
            program_name = "Cybersecurity (NATO-backed program)"
        elif country == "Germany":
            program_name = "Advanced Computer Security"
        elif country == "United States":
            program_name = "Computer Science with Cybersecurity focus"
        else:
            program_name = "Computer Science"
        
        variables = {
            "SCHOOL_NAME": school_name,
            "PROGRAM_NAME": program_name,
            "SPECIALIZED_AREA": specialized_area,
            "TARGET_COURSES": target_courses,
            "COURSE_1": university.get("notable_courses", [])[0] if university.get("notable_courses") else "Advanced Computer Security",
            "COURSE_2": university.get("notable_courses", [])[1] if len(university.get("notable_courses", [])) > 1 else "Machine Learning",
            "COURSE_3": university.get("notable_courses", [])[2] if len(university.get("notable_courses", [])) > 2 else "Quantum Computing",
            "ELECTIVE_1": "Network Security" if country == "Germany" else "AI Security",
            "ELECTIVE_2": "Cryptography" if "taltech" in school_name.lower() else "System Security",
            "PROFESSOR_NAME": professor_suggestions.split(",")[0].strip() if professor_suggestions else "Cybersecurity faculty",
            "COUNTRY": country
        }
        
        # 替換變數
        customized_content = self._replace_template_variables(template, variables)
        
        return customized_content
    
    def generate_cv(self, university: Dict[str, Any]) -> str:
        """生成客製化履歷"""
        template = self._load_template("cv_template.md")
        if not template:
            return ""
        
        # 根據學校特色調整履歷重點
        school_name = university.get("school_name", "Unknown University")
        country = university.get("country", "Unknown Country")
        
        # 根據學校特色決定強調的經驗
        if "taltech" in school_name.lower():
            focus_area = "NATO-backed Cybersecurity program"
            key_experience = "Critical infrastructure protection at TWSE"
        elif country == "Germany":
            focus_area = "Advanced Computer Security"
            key_experience = "Enterprise security solutions"
        elif country == "United States":
            focus_area = "AI-driven Security Systems"
            key_experience = "Cloud security and DevSecOps"
        else:
            focus_area = "Cybersecurity and Cloud Infrastructure"
            key_experience = "Full-stack security development"
        
        variables = {
            "FOCUS_AREA": focus_area,
            "KEY_EXPERIENCE": key_experience
        }
        
        # 替換變數
        customized_content = self._replace_template_variables(template, variables)
        
        return customized_content
    
    def generate_application_package(self, university: Dict[str, Any]) -> Dict[str, str]:
        """為單一學校生成完整申請文件包"""
        school_name = university.get("school_name", "Unknown")
        country = university.get("country", "Unknown")
        
        # 清理學校名稱，用於檔案名稱
        safe_school_name = re.sub(r'[^\w\s-]', '', school_name).strip()
        safe_school_name = re.sub(r'[-\s]+', '_', safe_school_name)
        
        # 生成文件
        study_plan = self.generate_study_plan(university)
        cv = self.generate_cv(university)
        
        # 準備輸出檔案名稱
        timestamp = datetime.now().strftime("%Y%m%d")
        study_plan_filename = f"{safe_school_name}_study_plan_{timestamp}.md"
        cv_filename = f"{safe_school_name}_cv_{timestamp}.md"
        
        # 確保輸出目錄存在
        school_output_dir = os.path.join(self.output_dir, safe_school_name)
        os.makedirs(school_output_dir, exist_ok=True)
        
        # 寫入文件
        study_plan_path = os.path.join(school_output_dir, study_plan_filename)
        cv_path = os.path.join(school_output_dir, cv_filename)
        
        with open(study_plan_path, 'w', encoding='utf-8') as file:
            file.write(study_plan)
        
        with open(cv_path, 'w', encoding='utf-8') as file:
            file.write(cv)
        
        return {
            "school_name": school_name,
            "study_plan_path": study_plan_path,
            "cv_path": cv_path,
            "output_directory": school_output_dir
        }
    
    def generate_all_applications(self, eligible_only: bool = True) -> List[Dict[str, Any]]:
        """為所有符合資格的學校生成申請文件"""
        results = []
        
        # 載入學校資料
        university_options = self._load_yaml("source_data/university_level_options.yml")
        college_options = self._load_yaml("source_data/college_level_options.yml")
        
        all_universities = []
        all_universities.extend(university_options.get("universities", []))
        all_universities.extend(college_options.get("universities", []))
        
        # 如果只要符合資格的學校，需要先執行資格驗證
        if eligible_only:
            # 這裡可以整合validator.py的結果
            # 暫時假設所有學校都符合資格
            pass
        
        # 為每個學校生成申請文件
        for university in all_universities:
            try:
                result = self.generate_application_package(university)
                results.append(result)
                print(f"已生成 {university['school_name']} 的申請文件")
            except Exception as e:
                print(f"生成 {university['school_name']} 申請文件時發生錯誤: {e}")
        
        return results
    
    def generate_dashboard(self, applications: List[Dict[str, Any]]) -> str:
        """生成申請進度儀表板"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        dashboard_content = f"""# 交換申請進度儀表板
*最後更新: {current_time}*

## 📊 申請總覽

| 學校名稱 | 國家 | 計畫類型 | 申請狀態 | 競爭分數 | 名額 | 文件狀態 |
|:---|:---|:---|:---|:---|:---|:---|
"""
        
        # 載入學校資料以獲取更多資訊
        university_options = self._load_yaml("source_data/university_level_options.yml")
        college_options = self._load_yaml("source_data/college_level_options.yml")
        
        all_universities = {}
        for uni in university_options.get("universities", []):
            all_universities[uni["school_name"]] = {**uni, "program_type": "校級"}
        for uni in college_options.get("universities", []):
            all_universities[uni["school_name"]] = {**uni, "program_type": "院級"}
        
        for app in applications:
            school_name = app["school_name"]
            uni_info = all_universities.get(school_name, {})
            
            dashboard_content += f"| {school_name} | {uni_info.get('country', 'Unknown')} | {uni_info.get('program_type', 'Unknown')} | {uni_info.get('application_status', 'Not Started')} | {uni_info.get('predicted_competition_score', 'N/A')}/10 | {uni_info.get('slots_available', 'N/A')} | ✅ 已生成 |\n"
        
        dashboard_content += f"""
## 📋 個人準備進度

- [ ] 英語檢定 (IELTS/TOEFL)
- [ ] 成績單申請
- [ ] 推薦信準備
- [x] 履歷 (CV) 準備
- [x] 讀書計畫準備
- [ ] 其他支持文件

## 📁 已生成文件

"""
        
        for app in applications:
            dashboard_content += f"""### {app['school_name']}
- 📄 讀書計畫: `{app['study_plan_path']}`
- 📄 履歷: `{app['cv_path']}`
- 📁 目錄: `{app['output_directory']}`

"""
        
        dashboard_content += """## 🎯 下一步行動

1. **立即行動**:
   - 準備英語檢定考試
   - 聯繫推薦人撰寫推薦信

2. **文件完善**:
   - 根據各校要求調整讀書計畫
   - 準備成績單和證照副本

3. **申請提交**:
   - 檢查各校申請截止日期
   - 準備線上申請系統資料

---
*此儀表板由 ExchangeApp-IAC 自動生成*
"""
        
        return dashboard_content

def main():
    """主函數"""
    print("開始生成申請文件...")
    
    # 檢查必要檔案是否存在
    required_files = ["my_profile.yml", "templates/study_plan_template.md", "templates/cv_template.md"]
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"缺少必要檔案: {', '.join(missing_files)}")
        return
    
    # 執行文件生成
    generator = DocumentGenerator()
    applications = generator.generate_all_applications()
    
    # 生成儀表板
    dashboard_content = generator.generate_dashboard(applications)
    dashboard_path = os.path.join(generator.output_dir, "dashboard.md")
    
    with open(dashboard_path, 'w', encoding='utf-8') as file:
        file.write(dashboard_content)
    
    print("文件生成完成!")
    print(f"儀表板位置: {dashboard_path}")
    print(f"共生成 {len(applications)} 所學校的申請文件")

if __name__ == "__main__":
    main()
