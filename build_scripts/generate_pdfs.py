#!/usr/bin/env python3
"""
Exchange Application PDF Generator
自動生成交換申請所需的PDF文件

依據 ISCTE 申請要求生成：
1. Curriculum Vitae (最大 4MB PDF)
2. Transcript of Records (最大 10MB PDF)  
3. Other Documents (最大 10MB PDF)

作者: Pei-Chen Lee
日期: 2025-10-10
"""

import os
import sys
import yaml
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# PDF generation libraries
try:
    import markdown
    from weasyprint import HTML, CSS
    from PIL import Image
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4, letter
    from reportlab.lib.utils import ImageReader
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
    from reportlab.lib.units import inch
    import img2pdf
except ImportError as e:
    print(f"❌ 缺少必要的Python套件: {e}")
    print("請執行: pip install markdown weasyprint pillow reportlab img2pdf")
    sys.exit(1)

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pdf_generation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PDFGenerator:
    """PDF生成器主類別"""
    
    def __init__(self, profile_path: str = "my_profile.yml"):
        self.profile_path = profile_path
        self.profile_data = self._load_profile()
        self.output_dir = Path("application_pdfs")
        self.output_dir.mkdir(exist_ok=True)
        
        # 建立日期時間戳
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        logger.info(f"🔧 PDF Generator 初始化完成")
        logger.info(f"📁 輸出目錄: {self.output_dir}")
        
    def _load_profile(self) -> Dict:
        """載入個人資料檔案"""
        try:
            with open(self.profile_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                logger.info(f"✅ 成功載入個人資料: {self.profile_path}")
                return data
        except FileNotFoundError:
            logger.error(f"❌ 找不到個人資料檔案: {self.profile_path}")
            sys.exit(1)
        except yaml.YAMLError as e:
            logger.error(f"❌ YAML檔案格式錯誤: {e}")
            sys.exit(1)
    
    def generate_cv_pdf(self) -> Path:
        """
        生成履歷PDF
        從final_applications中選擇最佳CV模板並轉換為PDF
        """
        logger.info("📄 開始生成履歷PDF...")
        
        # 尋找最新的CV檔案
        cv_files = list(Path("final_applications").glob("*/Stanford_University_cv_*.md"))
        if not cv_files:
            # 備用方案：使用模板
            cv_files = [Path("templates/cv_template.md")]
        
        if not cv_files:
            logger.error("❌ 找不到CV模板檔案")
            return None
            
        cv_file = cv_files[0]  # 使用最新的
        logger.info(f"📂 使用CV檔案: {cv_file}")
        
        # 讀取Markdown內容
        try:
            with open(cv_file, 'r', encoding='utf-8') as f:
                md_content = f.read()
                
            # 移除"交換申請履歷"字眼
            md_content = md_content.replace("交換申請履歷", "")
            md_content = md_content.replace("- 交換申請履歷", "")
            md_content = md_content.replace("交換申請", "Exchange Application")
                
        except Exception as e:
            logger.error(f"❌ 讀取CV檔案失敗: {e}")
            return None
        
        # 轉換為HTML
        html_content = markdown.markdown(md_content, extensions=['tables', 'nl2br'])
        
        # 加入CSS樣式
        css_style = """
        <style>
        body {
            font-family: 'Times New Roman', serif;
            font-size: 11pt;
            line-height: 1.4;
            margin: 0.8in;
            color: #333;
        }
        h1 {
            font-size: 18pt;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 5pt;
            margin-bottom: 15pt;
        }
        h2 {
            font-size: 14pt;
            color: #2c3e50;
            margin-top: 20pt;
            margin-bottom: 10pt;
        }
        h3 {
            font-size: 12pt;
            color: #34495e;
            margin-top: 15pt;
            margin-bottom: 8pt;
        }
        p {
            margin-bottom: 8pt;
            text-align: justify;
        }
        ul, ol {
            margin-bottom: 10pt;
        }
        li {
            margin-bottom: 3pt;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 15pt;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8pt;
            text-align: left;
        }
        th {
            background-color: #f8f9fa;
            font-weight: bold;
        }
        .contact-info {
            text-align: center;
            margin-bottom: 20pt;
        }
        @page {
            size: A4;
            margin: 0.8in;
        }
        </style>
        """
        
        # 組合完整HTML
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            {css_style}
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # 生成PDF
        output_path = self.output_dir / f"CV_PeiChen_Lee_{self.timestamp}.pdf"
        
        try:
            HTML(string=full_html).write_pdf(output_path)
            
            # 檢查檔案大小 (4MB限制)
            file_size = output_path.stat().st_size
            size_mb = file_size / (1024 * 1024)
            
            if size_mb > 4:
                logger.warning(f"⚠️ CV PDF大小超過限制: {size_mb:.2f}MB > 4MB")
            else:
                logger.info(f"✅ CV PDF生成成功: {output_path}")
                logger.info(f"📏 檔案大小: {size_mb:.2f}MB")
                
            return output_path
            
        except Exception as e:
            logger.error(f"❌ PDF生成失敗: {e}")
            return None
    
    def generate_transcript_pdf(self) -> Path:
        """
        生成成績單PDF
        將JPG掃描檔整合成單一PDF並加上說明頁
        """
        logger.info("📊 開始生成成績單PDF...")
        
        # 尋找成績單圖片
        transcript_dir = Path("supporting_documents/transcripts")
        if not transcript_dir.exists():
            transcript_dir = Path("Exchange student/成績單")
        
        if not transcript_dir.exists():
            logger.error("❌ 找不到成績單目錄")
            return None
        
        # 獲取所有JPG檔案
        image_files = list(transcript_dir.glob("*.jpg")) + list(transcript_dir.glob("*.JPG"))
        image_files.sort()  # 按檔名排序
        
        if not image_files:
            logger.error("❌ 找不到成績單圖片檔案")
            return None
            
        logger.info(f"📷 找到 {len(image_files)} 張成績單圖片")
        
        output_path = self.output_dir / f"Transcript_Records_PeiChen_Lee_{self.timestamp}.pdf"
        
        try:
            # 建立PDF文件
            doc = SimpleDocTemplate(str(output_path), pagesize=A4)
            story = []
            styles = getSampleStyleSheet()
            
            # 標題頁
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=20,
                alignment=1  # 置中
            )
            
            story.append(Paragraph("TRANSCRIPT OF RECORDS", title_style))
            story.append(Paragraph(f"Student: {self.profile_data['personal_info']['english_name']}", styles['Normal']))
            story.append(Paragraph(f"University: {self.profile_data['education']['current_program']['university']}", styles['Normal']))
            story.append(Paragraph(f"Program: {self.profile_data['education']['current_program']['program']}", styles['Normal']))
            story.append(Paragraph(f"GPA: {self.profile_data['education']['current_program']['gpa']}/{self.profile_data['education']['current_program']['max_gpa']} ({self.profile_data['education']['current_program']['gpa_percentage']:.1f}%)", styles['Normal']))
            story.append(Paragraph(f"Class Ranking: {self.profile_data['education']['current_program']['class_ranking']}", styles['Normal']))
            story.append(Spacer(1, 20))
            
            # 說明文字 - 更好地區分大學和碩士狀態
            explanation = """
            <b>Document Explanation:</b><br/>
            The following pages contain scanned copies of official transcripts from National Chengchi University (NCCU).
            These documents include academic records from both undergraduate and graduate programs.
            
            <br/><br/>
            <b>Educational Background:</b><br/>
            • <b>Undergraduate Degree:</b> Computer Science - <b>COMPLETED (Graduated)</b><br/>
            • <b>Graduate Program:</b> Digital Content and Technologies - <b>COURSEWORK COMPLETED (Currently completing thesis)</b><br/>
            
            <br/><br/>
            <b>Note:</b> Official English transcripts have been requested from NCCU Registrar's Office and will be submitted separately upon receipt.
            
            <br/><br/>
            <b>Academic Performance Summary:</b><br/>
            • Graduate Program GPA: 3.96/4.3 (92.09%)<br/>
            • Class Ranking: Top 5% (Graduate Program)<br/>
            • Graduate Program Duration: September 2021 - June 2023<br/>
            • Current Status: <b>Graduate coursework completed, thesis in progress</b><br/>
            • Expected Graduation: June 2025
            """
            
            story.append(Paragraph(explanation, styles['Normal']))
            story.append(Spacer(1, 30))
            
            # 加入成績單圖片
            for i, img_file in enumerate(image_files, 1):
                story.append(Paragraph(f"<b>Transcript Page {i}:</b>", styles['Heading2']))
                
                # 調整圖片大小以適應頁面
                try:
                    img = Image.open(img_file)
                    img_width, img_height = img.size
                    
                    # 計算適合的大小 (保持比例)
                    max_width = 6 * inch
                    max_height = 8 * inch
                    
                    ratio = min(max_width/img_width, max_height/img_height)
                    new_width = img_width * ratio
                    new_height = img_height * ratio
                    
                    rl_img = RLImage(str(img_file), width=new_width, height=new_height)
                    story.append(rl_img)
                    story.append(Spacer(1, 20))
                    
                except Exception as e:
                    logger.error(f"❌ 處理圖片失敗 {img_file}: {e}")
                    continue
            
            # 建立PDF
            doc.build(story)
            
            # 檢查檔案大小 (10MB限制)
            file_size = output_path.stat().st_size
            size_mb = file_size / (1024 * 1024)
            
            if size_mb > 10:
                logger.warning(f"⚠️ 成績單PDF大小超過限制: {size_mb:.2f}MB > 10MB")
            else:
                logger.info(f"✅ 成績單PDF生成成功: {output_path}")
                logger.info(f"📏 檔案大小: {size_mb:.2f}MB")
                
            return output_path
            
        except Exception as e:
            logger.error(f"❌ 成績單PDF生成失敗: {e}")
            return None
    
    def generate_supporting_documents_pdf(self) -> Path:
        """
        生成其他支持文件PDF
        整合證照、獎項、作品集等資料
        """
        logger.info("📎 開始生成支持文件PDF...")
        
        output_path = self.output_dir / f"Supporting_Documents_PeiChen_Lee_{self.timestamp}.pdf"
        
        try:
            doc = SimpleDocTemplate(str(output_path), pagesize=A4)
            story = []
            styles = getSampleStyleSheet()
            
            # 讀取支持文件索引
            try:
                with open("supporting_documents/SUPPORTING_DOCUMENTS_INDEX.md", 'r', encoding='utf-8') as f:
                    index_content = f.read()
                    
                # 轉換為HTML再轉為PDF內容
                html_content = markdown.markdown(index_content, extensions=['tables', 'nl2br'])
                
                # 簡化處理：將HTML轉為純文字段落
                # 這裡可以進一步優化HTML到ReportLab的轉換
                
                # 標題
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Heading1'],
                    fontSize=16,
                    spaceAfter=20,
                    alignment=1
                )
                
                story.append(Paragraph("SUPPORTING DOCUMENTS", title_style))
                story.append(Paragraph(f"Applicant: {self.profile_data['personal_info']['english_name']}", styles['Normal']))
                story.append(Paragraph(f"Application Date: {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
                story.append(Spacer(1, 30))
                
                # 摘要
                summary = f"""
                <b>DOCUMENT SUMMARY</b><br/><br/>
                
                This document package contains supporting evidence for the exchange application of 
                {self.profile_data['personal_info']['english_name']}. The materials are organized to provide 
                comprehensive documentation of academic achievements, professional certifications, 
                cross-cultural experiences, and technical capabilities.
                
                <br/><br/>
                <b>KEY HIGHLIGHTS:</b><br/>
                • 45+ Professional Certifications (Security, Cloud, Quantum Computing)<br/>
                • IELTS 7.0 (Reading 9.0/9.0)<br/>
                • Graduate Student Scholarship Recipient<br/>
                • International Development Experience (TaiwanICDF - Somaliland)<br/>
                • Cross-Cultural Performance Tour (Japan)<br/>
                • NFT Art Exhibition Participant<br/>
                • Active GitHub Contributor (2,500+ commits/year)
                
                <br/><br/>
                <b>PROFESSIONAL EXPERIENCE:</b><br/>
                • Cybersecurity Developer at MITAKE Information Co., Ltd.<br/>
                • Led critical infrastructure protection (TWSE, Cathay Financial)<br/>
                • Healthcare IT Systems Development (FHIR/HL7)<br/>
                • Quantum Computing Research & Implementation
                """
                
                story.append(Paragraph(summary, styles['Normal']))
                story.append(Spacer(1, 30))
                
                # 證照摘要
                cert_summary = """
                <b>CERTIFICATION HIGHLIGHTS:</b><br/><br/>
                
                <b>Security & Cybersecurity:</b><br/>
                • ISC² Certified in Cybersecurity (CC) - 2025-2028<br/>
                • Cloudflare ACE/ASE/MSP Certifications - 2024-2026<br/>
                • Prisma Cloud Risk Prevention & Runtime Protection<br/>
                • DSPM Fundamentals (Securiti)<br/><br/>
                
                <b>Cloud Platforms:</b><br/>
                • AWS Cloud Practitioner & Security Fundamentals<br/>
                • Google Cloud Platform (GCP) - Kubernetes & Security<br/>
                • Oracle Cloud Infrastructure 2024 Foundations<br/><br/>
                
                <b>Quantum Computing:</b><br/>
                • Linux Foundation Quantum Computing (LFQ101)<br/>
                • IBM Quantum Business Foundations & Algorithm Design<br/>
                • Microsoft Azure Quantum<br/>
                • Practical Quantum-Safe Cryptography<br/><br/>
                
                <b>Healthcare IT:</b><br/>
                • Johns Hopkins Healthcare IT Support Specialization<br/>
                • ICD-10 Certification (CMS)<br/>
                • FHIR/HL7 Implementation Experience
                """
                
                story.append(Paragraph(cert_summary, styles['Normal']))
                story.append(Spacer(1, 20))
                
                # 加入證照文件從 certifications 目錄
                self._add_certifications_to_story(story, styles)
                
                # 加入支持圖片 (如果存在)
                support_images = [
                    "supporting_documents/獎學金.png",
                    "supporting_documents/Github-achivement-1.png", 
                    "supporting_documents/Github-achivement-2.png",
                    "supporting_documents/校園事務參與.png"
                ]
                
                for img_path in support_images:
                    if Path(img_path).exists():
                        try:
                            story.append(Paragraph(f"<b>Evidence: {Path(img_path).stem}</b>", styles['Heading3']))
                            
                            # 調整圖片大小
                            img = Image.open(img_path)
                            img_width, img_height = img.size
                            
                            max_width = 6 * inch
                            max_height = 4 * inch
                            
                            ratio = min(max_width/img_width, max_height/img_height)
                            new_width = img_width * ratio
                            new_height = img_height * ratio
                            
                            rl_img = RLImage(img_path, width=new_width, height=new_height)
                            story.append(rl_img)
                            story.append(Spacer(1, 15))
                            
                        except Exception as e:
                            logger.warning(f"⚠️ 無法加入圖片 {img_path}: {e}")
                
                # 聯絡資訊
                contact_info = f"""
                <br/><br/>
                <b>CONTACT INFORMATION</b><br/>
                Email: {self.profile_data['personal_info']['email']}<br/>
                Phone: {self.profile_data['personal_info']['phone']}<br/>
                Portfolio: {self.profile_data['personal_info']['portfolio']}<br/>
                LinkedIn: {self.profile_data['personal_info']['linkedin']}<br/>
                GitHub: {self.profile_data['personal_info']['github']}
                
                <br/><br/>
                <i>For detailed information about certifications, projects, and achievements, 
                please refer to the online portfolio and GitHub repositories.</i>
                """
                
                story.append(Paragraph(contact_info, styles['Normal']))
                
            except FileNotFoundError:
                logger.warning("⚠️ 找不到支持文件索引，使用基本模板")
                story.append(Paragraph("Supporting Documents Package", styles['Title']))
                story.append(Paragraph("Complete documentation available in online portfolio.", styles['Normal']))
            
            # 建立PDF
            doc.build(story)
            
            # 檢查檔案大小
            file_size = output_path.stat().st_size
            size_mb = file_size / (1024 * 1024)
            
            if size_mb > 10:
                logger.warning(f"⚠️ 支持文件PDF大小超過限制: {size_mb:.2f}MB > 10MB")
            else:
                logger.info(f"✅ 支持文件PDF生成成功: {output_path}")
                logger.info(f"📏 檔案大小: {size_mb:.2f}MB")
                
            return output_path
            
        except Exception as e:
            logger.error(f"❌ 支持文件PDF生成失敗: {e}")
            return None
    
    def generate_all_pdfs(self) -> Dict[str, Optional[Path]]:
        """生成所有PDF文件"""
        logger.info("🚀 開始生成所有申請PDF文件...")
        
        results = {
            'cv': self.generate_cv_pdf(),
            'transcript': self.generate_transcript_pdf(),
            'supporting_docs': self.generate_supporting_documents_pdf()
        }
        
        # 總結報告
        logger.info("\n" + "="*60)
        logger.info("📋 PDF生成結果總結:")
        logger.info("="*60)
        
        success_count = 0
        for doc_type, path in results.items():
            if path and path.exists():
                size_mb = path.stat().st_size / (1024 * 1024)
                logger.info(f"✅ {doc_type.upper()}: {path.name} ({size_mb:.2f}MB)")
                success_count += 1
            else:
                logger.error(f"❌ {doc_type.upper()}: 生成失敗")
        
        logger.info(f"\n🎯 成功生成 {success_count}/3 個PDF文件")
        logger.info(f"📁 輸出目錄: {self.output_dir.absolute()}")
        
        return results
    
    def _add_certifications_to_story(self, story, styles):
        """加入證照文件到PDF中"""
        cert_dir = Path("supporting_documents/certifications")
        if not cert_dir.exists():
            logger.warning("⚠️ 找不到certifications目錄")
            return
            
        logger.info(f"📜 正在加入證照文件...")
        
        # 加入證照章節標題
        cert_title = ParagraphStyle(
            'CertTitle',
            parent=styles['Heading1'],
            fontSize=14,
            spaceAfter=15,
            textColor='#2c3e50'
        )
        
        story.append(Paragraph("<b>PROFESSIONAL CERTIFICATIONS</b>", cert_title))
        story.append(Spacer(1, 10))
        
        # 獲取所有證照文件
        cert_files = []
        for ext in ['*.pdf', '*.png', '*.jpg', '*.jpeg']:
            cert_files.extend(list(cert_dir.glob(ext)))
        
        # 過濾掉不需要的文件
        excluded_files = ['CERTIFICATIONS_INDEX.md']
        cert_files = [f for f in cert_files if f.name not in excluded_files]
        
        # 依重要性排序（重要證照先顯示）
        priority_certs = ['CC.pdf', 'AI-SECURITY.pdf', 'TW00125503682-03-10-2025-ETRF.pdf']
        sorted_files = []
        
        # 先加入優先證照
        for priority in priority_certs:
            for cert_file in cert_files:
                if cert_file.name == priority:
                    sorted_files.append(cert_file)
                    break
        
        # 加入其他證照（最多10個避免檔案過大）
        other_certs = [f for f in cert_files if f not in sorted_files]
        sorted_files.extend(other_certs[:10])  # 限制總數
        
        logger.info(f"📊 找到 {len(cert_files)} 個證照文件，將嵌入 {len(sorted_files)} 個")
        
        cert_count = 0
        for cert_file in sorted_files:
            try:
                cert_count += 1
                
                # 證照名稱
                cert_name = cert_file.stem.replace('_', ' ').replace('-', ' ')
                story.append(Paragraph(f"<b>{cert_count}. {cert_name}</b>", styles['Heading3']))
                
                if cert_file.suffix.lower() == '.pdf':
                    # PDF檔案：提供檔案資訊
                    file_info = f"證照文件: {cert_file.name} (PDF Format)"
                    story.append(Paragraph(file_info, styles['Normal']))
                    
                    # 試圖讀取PDF的第一頁作為縮圖（可選）
                    story.append(Paragraph("<i>PDF certificate file included in digital submission.</i>", styles['Normal']))
                    
                else:
                    # 圖片檔案：嵌入圖片
                    img = Image.open(cert_file)
                    img_width, img_height = img.size
                    
                    # 調整大小以適合頁面
                    max_width = 5 * inch
                    max_height = 6 * inch
                    
                    ratio = min(max_width/img_width, max_height/img_height)
                    new_width = img_width * ratio
                    new_height = img_height * ratio
                    
                    rl_img = RLImage(str(cert_file), width=new_width, height=new_height)
                    story.append(rl_img)
                
                story.append(Spacer(1, 15))
                
                # 每3個證照後加一個分頁（避免內容過擠）
                if cert_count % 3 == 0:
                    from reportlab.platypus import PageBreak
                    story.append(PageBreak())
                    
            except Exception as e:
                logger.warning(f"⚠️ 無法處理證照文件 {cert_file}: {e}")
                continue
        
        # 證照總結
        summary_text = f"""
        <br/><br/>
        <b>Certification Summary:</b><br/>
        • Total Certifications Included: {cert_count}<br/>
        • Fields Covered: Cybersecurity, Cloud Computing, Quantum Computing, AI Security<br/>
        • Issuing Organizations: ISC², AWS, Google Cloud, Coursera, edX, IBM<br/>
        • Certification Period: 2022-2025 (Active)<br/><br/>
        
        <i>All certifications are current and valid. Complete certification details 
        and verification links are available in the digital portfolio.</i>
        """
        
        story.append(Paragraph(summary_text, styles['Normal']))
        story.append(Spacer(1, 20))

def main():
    """主函式"""
    parser = argparse.ArgumentParser(description="生成交換申請PDF文件")
    parser.add_argument("--profile", default="my_profile.yml", help="個人資料檔案路徑")
    parser.add_argument("--type", choices=['cv', 'transcript', 'supporting', 'all'], 
                       default='all', help="要生成的PDF類型")
    parser.add_argument("--output", help="輸出目錄")
    
    args = parser.parse_args()
    
    try:
        generator = PDFGenerator(args.profile)
        
        if args.output:
            generator.output_dir = Path(args.output)
            generator.output_dir.mkdir(exist_ok=True)
        
        if args.type == 'cv':
            generator.generate_cv_pdf()
        elif args.type == 'transcript':
            generator.generate_transcript_pdf()
        elif args.type == 'supporting':
            generator.generate_supporting_documents_pdf()
        else:  # all
            generator.generate_all_pdfs()
            
        logger.info("🎉 PDF生成流程完成！")
        
    except KeyboardInterrupt:
        logger.info("⏹️ 用戶中斷操作")
    except Exception as e:
        logger.error(f"💥 發生未預期的錯誤: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
