import os
import re
from pathlib import Path

base_dir = Path(r"d:\Programs\Androide\websites\MishalCo")

# قائمة جميع ملفات HTML
html_files = list(base_dir.glob("*.html"))
html_files.extend(base_dir.glob("blogs/*.html"))

print("="*70)
print("🔄 FINAL IMAGE CONVERSION TO WEBP")
print("="*70)
print(f"\nProcessing {len(html_files)} HTML files...\n")

total_changes = 0
files_updated = 0

for html_file in html_files:
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        changes = 0
        
        # استبدال جميع الصور JPG/PNG/JPEG بـ WebP
        # نمط 1: src="path/image.jpg"
        patterns = [
            (r'src="(assets/img/[^"]+)\.jpg"', r'src="\1.webp"'),
            (r'src="(assets/img/[^"]+)\.jpeg"', r'src="\1.webp"'),
            (r'src="(assets/img/[^"]+)\.png"', r'src="\1.webp"'),
            (r'src="\.\./assets/img/([^"]+)\.jpg"', r'src="../assets/img/\1.webp"'),
            (r'src="\.\./assets/img/([^"]+)\.jpeg"', r'src="../assets/img/\1.webp"'),
            (r'src="\.\./assets/img/([^"]+)\.png"', r'src="../assets/img/\1.webp"'),
            # نمط 2: href="path/image.jpg" (للروابط في galleries)
            (r'href="(assets/img/[^"]+)\.jpg"', r'href="\1.webp"'),
            (r'href="(assets/img/[^"]+)\.jpeg"', r'href="\1.webp"'),
            (r'href="(assets/img/[^"]+)\.png"', r'href="\1.webp"'),
            (r'href="\.\./assets/img/([^"]+)\.jpg"', r'href="../assets/img/\1.webp"'),
            (r'href="\.\./assets/img/([^"]+)\.jpeg"', r'href="../assets/img/\1.webp"'),
            (r'href="\.\./assets/img/([^"]+)\.png"', r'href="../assets/img/\1.webp"'),
        ]
        
        for pattern, replacement in patterns:
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                count = len(re.findall(pattern, content))
                changes += count
                content = new_content
        
        # حفظ الملف إذا تم إجراء تغييرات
        if content != original:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ {html_file.name}")
            print(f"   └─ {changes} images converted to WebP")
            files_updated += 1
            total_changes += changes
        
    except Exception as e:
        print(f"❌ Error: {html_file.name} - {e}")

print("\n" + "="*70)
print("📊 FINAL SUMMARY")
print("="*70)
print(f"✅ Files updated: {files_updated}")
print(f"🔄 Total images converted: {total_changes}")
print(f"📁 Total files scanned: {len(html_files)}")
print("="*70)
print("\n✨ All images successfully converted to WebP format!")
print("\n🎯 Next steps:")
print("   1. Test the website locally")
print("   2. Upload all files to server")
print("   3. Test on Google PageSpeed Insights")
print("="*70)
