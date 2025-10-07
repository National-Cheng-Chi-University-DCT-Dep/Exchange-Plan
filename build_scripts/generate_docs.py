#!/usr/bin/env python3
"""
文件生成腳本 - Exchange Application Document Generator
根據 my_profile.yml 和交換機會資料自動生成客製化申請文件

Usage:
    python generate_docs.py --university "University of Bern" --type cv
    python generate_docs.py --university "UC San Diego" --type study_plan
    python generate_docs.py --all  # 生成所有文件
"""

import yaml
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

# 專案根目錄
PROJECT_ROOT = Path(__file__).parent.parent

def load_profile():
    """載入個人profile資料"""
    profile_path = PROJECT_ROOT / "my_profile.yml"
    with open(profile_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_template(template_name):
    """載入模板文件"""
    template_path = PROJECT_ROOT / "templates" / template_name
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

def generate_cv(profile, university=None):
    """生成CV文件"""
    print(f"生成 CV for {university or 'General'}...")
    
    # 載入CV模板
    template = load_template("cv_template.md")
    
    # 準備變量替換
    personal_info = profile['personal_info']
    education = profile['education']
    
    # 基本資訊替換
    cv_content = template.replace("{{APPLICANT_NAME}}", personal_info['english_name'])
    cv_content = cv_content.replace("{{LOCATION}}", "Taipei, Taiwan")
    cv_content = cv_content.replace("{{PHONE}}", personal_info['phone'])
    cv_content = cv_content.replace("{{EMAIL}}", personal_info['email'])
    cv_content = cv_content.replace("{{PORTFOLIO_URL}}", personal_info['portfolio'])
    cv_content = cv_content.replace("{{LINKEDIN_URL}}", personal_info['linkedin'])
    cv_content = cv_content.replace("{{GITHUB_URL}}", personal_info['github'])
    
    # Academic Profile
    academic_profile = f"A Master's student in Digital Content & Technology with five years of professional experience in Cloud Infrastructure and Cybersecurity. Dedicated to exploring the intersection of quantum computing, AI ethics, and post-quantum cryptography. Seeking an exchange opportunity to advance research on {profile['research_interests']['primary'][0]}."
    cv_content = cv_content.replace("{{ACADEMIC_PROFILE_SUMMARY}}", academic_profile)
    
    # 教育背景
    current_edu = education['current_program']
    cv_content = cv_content.replace("{{CURRENT_UNIVERSITY}}", current_edu['university'])
    cv_content = cv_content.replace("{{CURRENT_LOCATION}}", "Taipei, Taiwan")
    cv_content = cv_content.replace("{{CURRENT_DEGREE}}", current_edu['degree_type'])
    cv_content = cv_content.replace("{{CURRENT_PROGRAM}}", current_edu['program'])
    cv_content = cv_content.replace("{{CURRENT_START_DATE}}", current_edu['start_date'])
    cv_content = cv_content.replace("{{CURRENT_END_DATE}}", current_edu['end_date'])
    cv_content = cv_content.replace("{{GPA}}", str(current_edu['gpa']))
    cv_content = cv_content.replace("{{MAX_GPA}}", str(current_edu['max_gpa']))
    cv_content = cv_content.replace("{{GPA_PERCENTAGE}}", str(current_edu['gpa_percentage']))
    cv_content = cv_content.replace("{{CLASS_RANKING}}", current_edu['class_ranking'])
    
    undergrad = education['undergraduate']
    cv_content = cv_content.replace("{{UNDERGRADUATE_UNIVERSITY}}", undergrad['university'])
    cv_content = cv_content.replace("{{UNDERGRADUATE_LOCATION}}", "Taipei, Taiwan")
    cv_content = cv_content.replace("{{UNDERGRADUATE_DEGREE}}", undergrad['degree_type'])
    cv_content = cv_content.replace("{{UNDERGRADUATE_PROGRAM}}", undergrad['program'])
    cv_content = cv_content.replace("{{UNDERGRADUATE_START_DATE}}", undergrad['start_date'])
    cv_content = cv_content.replace("{{UNDERGRADUATE_END_DATE}}", undergrad['end_date'])
    
    # 論文研究
    thesis = profile['research_interests']['thesis']
    cv_content = cv_content.replace("{{THESIS_TITLE}}", thesis['title'])
    cv_content = cv_content.replace("{{THESIS_STATUS}}", "In Progress")
    cv_content = cv_content.replace("{{THESIS_DESCRIPTION}}", thesis['description'])
    cv_content = cv_content.replace("{{THESIS_METHODOLOGY}}", thesis['methodology'])
    cv_content = cv_content.replace("{{THESIS_GITHUB_URL}}", thesis['github_url'])
    
    # 工作經驗
    current_job = profile['professional_experience']['current_position']
    cv_content = cv_content.replace("{{CURRENT_JOB_TITLE}}", current_job['title'])
    cv_content = cv_content.replace("{{CURRENT_COMPANY}}", current_job['company'])
    cv_content = cv_content.replace("{{CURRENT_JOB_LOCATION}}", current_job['location'])
    cv_content = cv_content.replace("{{CURRENT_JOB_PERIOD}}", f"{current_job['start_date']} – {current_job['end_date']}")
    
    # 語言能力
    ielts = profile['language_proficiency']['english']['ielts']
    cv_content = cv_content.replace("{{IELTS_OVERALL}}", str(ielts['overall_score']))
    cv_content = cv_content.replace("{{IELTS_LISTENING}}", str(ielts['listening']))
    cv_content = cv_content.replace("{{IELTS_READING}}", str(ielts['reading']))
    cv_content = cv_content.replace("{{IELTS_WRITING}}", str(ielts['writing']))
    cv_content = cv_content.replace("{{IELTS_SPEAKING}}", str(ielts['speaking']))
    
    ef_set = profile['language_proficiency']['english']['ef_set']
    cv_content = cv_content.replace("{{EF_SET_SCORE}}", str(ef_set['score']))
    cv_content = cv_content.replace("{{EF_SET_LEVEL}}", ef_set['level'])
    
    # GitHub統計（示例數據）
    cv_content = cv_content.replace("{{GITHUB_COMMITS}}", "2,500+")
    cv_content = cv_content.replace("{{GITHUB_STARS}}", "222")
    cv_content = cv_content.replace("{{GITHUB_FOLLOWERS}}", "42")
    cv_content = cv_content.replace("{{GITHUB_CONTRIBUTION_PERCENT}}", "80")
    
    # 更新日期
    cv_content = cv_content.replace("{{UPDATE_DATE}}", datetime.now().strftime("%B %d, %Y"))
    
    # 簡化處理：移除未填充的模板標籤
    import re
    cv_content = re.sub(r'\{\{#.*?\}\}.*?\{\{/.*?\}\}', '', cv_content, flags=re.DOTALL)
    cv_content = re.sub(r'\{\{.*?\}\}', '[TO BE FILLED]', cv_content)
    
    # 儲存文件
    university_name = university.replace(" ", "_") if university else "General"
    output_dir = PROJECT_ROOT / "final_applications" / university_name
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f"{university_name}_cv_{datetime.now().strftime('%Y%m%d')}.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(cv_content)
    
    print(f"✅ CV generated: {output_file}")
    return output_file

def generate_study_plan(profile, university):
    """生成學習計畫書"""
    print(f"生成 Study Plan for {university}...")
    
    template = load_template("study_plan_template.md")
    
    # 基本資訊
    personal_info = profile['personal_info']
    prefs = profile['exchange_preferences']
    
    # 判斷是第一志願還是第二志願
    is_first_choice = university == prefs['target_universities']['first_choice']['university']
    
    if is_first_choice:
        uni_info = prefs['target_universities']['first_choice']
    else:
        uni_info = prefs['target_universities']['second_choice']
    
    # 替換基本信息
    plan_content = template.replace("{{APPLICANT_NAME}}", personal_info['english_name'])
    plan_content = plan_content.replace("{{MOTIVATION_TITLE}}", "從資安實踐者到前瞻技術探索者：一場必要的國際暖機")
    
    # 替換志願學校
    plan_content = plan_content.replace("{{FIRST_CHOICE_UNIVERSITY}}", prefs['target_universities']['first_choice']['university'])
    plan_content = plan_content.replace("{{SECOND_CHOICE_UNIVERSITY}}", prefs['target_universities']['second_choice']['university'])
    
    # 研究主題
    plan_content = plan_content.replace("{{RESEARCH_TOPIC}}", profile['research_interests']['primary'][0])
    
    # 簡化處理未填充標籤
    import re
    plan_content = re.sub(r'\{\{#.*?\}\}.*?\{\{/.*?\}\}', '', plan_content, flags=re.DOTALL)
    plan_content = re.sub(r'\{\{.*?\}\}', '[TO BE FILLED]', plan_content)
    
    # 儲存文件
    university_name = university.replace(" ", "_")
    output_dir = PROJECT_ROOT / "final_applications" / university_name
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f"{university_name}_study_plan_{datetime.now().strftime('%Y%m%d')}.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(plan_content)
    
    print(f"✅ Study Plan generated: {output_file}")
    return output_file

def main():
    parser = argparse.ArgumentParser(description='生成交換申請文件')
    parser.add_argument('--university', type=str, help='目標大學名稱')
    parser.add_argument('--type', type=str, choices=['cv', 'study_plan', 'both'], 
                       default='both', help='生成文件類型')
    parser.add_argument('--all', action='store_true', help='為所有目標大學生成文件')
    
    args = parser.parse_args()
    
    # 載入profile
    profile = load_profile()
    
    universities = []
    if args.all:
        # 為兩個志願都生成
        universities = [
            profile['exchange_preferences']['target_universities']['first_choice']['university'],
            profile['exchange_preferences']['target_universities']['second_choice']['university']
        ]
    elif args.university:
        universities = [args.university]
    else:
        print("請指定 --university 或使用 --all 參數")
        return
    
    for uni in universities:
        if args.type in ['cv', 'both']:
            generate_cv(profile, uni)
        
        if args.type in ['study_plan', 'both']:
            generate_study_plan(profile, uni)
    
    print("\n✨ 文件生成完成！")
    print(f"📁 輸出目錄: {PROJECT_ROOT / 'final_applications'}")

if __name__ == "__main__":
    main()

