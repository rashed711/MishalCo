import os
import re
from pathlib import Path

base_dir = Path(r"d:\Programs\Androide\websites\MishalCo")

# قائمة جميع ملفات HTML في المشروع
html_files = list(base_dir.glob("*.html"))
html_files.extend(base_dir.glob("blogs/*.html"))

print("="*70)
print("🔄 CONVERTING IMAGE REFERENCES TO WEBP")
print("="*70)
print(f"\nFound {len(html_files)} HTML files to process\n")

total_replacements = 0
files_modified = 0

for html_file in html_files:
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        file_replacements = 0
        
        # قائمة الأنماط للاستبدال
        # نستبدل فقط الصور التي لا تزال تشير إلى JPG/PNG
        # ولكن لديها نسخة WebP (تم حذف الأصلية)
        
        patterns = [
            # Hero carousel images
            (r'src="assets/img/hero-carousel/hero-carousel-(\d+)\.jpg"', 
             r'src="assets/img/hero-carousel/hero-carousel-\1.webp"'),
            
            # Team images
            (r'src="assets/img/team/team-(\d+)\.jpg"', 
             r'src="assets/img/team/team-\1.webp"'),
            
            # Construction/article images
            (r'src="assets/img/constructions-(\d+)\.jpg"', 
             r'src="assets/img/constructions-\1.webp"'),
            
            # Logo
            (r'src="assets/img/logo\.png"', 
             r'src="assets/img/logo.webp"'),
            
            # WhatsApp
            (r'src="assets/img/whatsapp\.png"', 
             r'src="assets/img/whatsapp.webp"'),
            
            # Alt services
            (r'src="assets/img/alt-services\.jpg"', 
             r'src="assets/img/alt-services.webp"'),
            
            # Page title background
            (r'url\(assets/img/page-title-bg\.jpg\)', 
             r'url(assets/img/page-title-bg.webp)'),
            
            # Features images
            (r'src="assets/img/features-(\d+)\.jpg"', 
             r'src="assets/img/features-\1.webp"'),
            
            # Footer background
            (r'url\(assets/img/footer-bg\.jpg\)', 
             r'url(assets/img/footer-bg.webp)'),
            
            # Type of case images - مجلد الخدمات
            (r'src="assets/img/type-of-case/([^"]+)\.jpg"', 
             r'src="assets/img/type-of-case/\1.webp"'),
            (r'src="assets/img/type-of-case/([^"]+)\.jpeg"', 
             r'src="assets/img/type-of-case/\1.webp"'),
        ]
        
        # تطبيق جميع الاستبدالات
        for pattern, replacement in patterns:
            matches = re.findall(pattern, content)
            if matches:
                content = re.sub(pattern, replacement, content)
                file_replacements += len(matches)
        
        # حفظ الملف إذا تم إجراء تغييرات
        if content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ {html_file.name}")
            print(f"   └─ {file_replacements} image references updated")
            
            files_modified += 1
            total_replacements += file_replacements
        
    except Exception as e:
        print(f"❌ Error processing {html_file.name}: {e}")

print("\n" + "="*70)
print("📊 CONVERSION SUMMARY")
print("="*70)
print(f"✅ Files modified: {files_modified}")
print(f"🔄 Total replacements: {total_replacements}")
print(f"📁 Total files scanned: {len(html_files)}")
print("="*70)
print("\n✨ All image references updated to WebP!")
