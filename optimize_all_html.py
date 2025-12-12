import os
import re
from pathlib import Path

base_dir = Path(r"d:\Programs\Androide\websites\MishalCo")

# قائمة جميع ملفات HTML
html_files = [
    'contact.html',
    'book_consultation.html',
    'Complaints.html',
    'FAQ.html',
    'blog.html',
    'projects.html',
    'photosss.html',
    '404.html',
    'blog-details-2025-01-01.html'
]

def optimize_page(file_path):
    """تحسين صفحة HTML واحدة"""
    print(f"\n{'='*60}")
    print(f"Processing: {file_path.name}")
    print(f"{'='*60}")
    
    if not file_path.exists():
        print(f"❌ File not found!")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changes = []
    
    # 1. تحويل الشعار إلى WebP
    if '<img src="assets/img/logo.png"' in content and '<picture>' not in content[:2000]:
        content = content.replace(
            '<img src="assets/img/logo.png" alt="مشعل بادغيش">',
            '''<picture>
          <source srcset="assets/img/logo.webp" type="image/webp">
          <img src="assets/img/logo.png" alt="مشعل بادغيش">
        </picture>'''
        )
        changes.append("✓ Logo → WebP")
    
    # 2. إضافة defer للسكربتات
    scripts_to_defer = [
        'bootstrap.bundle.min.js',
        'aos.js',
        'glightbox.min.js',
        'purecounter_vanilla.js',
        'swiper-bundle.min.js',
        'jquery',
        'isotope.pkgd.min.js',
        'imagesloaded.pkgd.min.js',
        'main.js'
    ]
    
    for script in scripts_to_defer:
        # ابحث عن السكربت بدون defer
        pattern = f'<script src="([^"]*{re.escape(script)}[^"]*)">'
        if re.search(pattern, content):
            content = re.sub(pattern, r'<script src="\1" defer>', content)
            if "defer" not in changes:
                changes.append("✓ Added defer to scripts")
    
    # 3. تحويل صورة الواتساب
    if 'whatsapp.png' in content and 'whatsapp.webp' not in content:
        # نمط أكثر مرونة
        whatsapp_patterns = [
            (r'<img src="assets/img/whatsapp\.png" alt="WhatsApp" class="whatsapp-icon"([^>]*)>',
             '''<picture>
      <source srcset="assets/img/whatsapp.webp" type="image/webp">
      <img src="assets/img/whatsapp.png" alt="WhatsApp" class="whatsapp-icon"\1>
    </picture>'''),
            (r'<img src="assets/img/whatsapp\.png" alt="([^"]*)" class="whatsapp-icon">',
             '''<picture>
      <source srcset="assets/img/whatsapp.webp" type="image/webp">
      <img src="assets/img/whatsapp.png" alt="\1" class="whatsapp-icon">
    </picture>''')
        ]
        
        for pattern, replacement in whatsapp_patterns:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                changes.append("✓ WhatsApp → WebP")
                break
    
    # 4. إضافة loading="lazy" للصور
    # نبحث عن جميع صور JPG/PNG بدون lazy loading
    img_pattern = r'<img\s+src="assets/img/([^"]+\.(jpg|png))"([^>]*?)(?<!loading="lazy")>'
    
    def add_lazy(match):
        src = match.group(1)
        ext = match.group(2)
        attrs = match.group(3)
        
        # تخطي الصور التي لديها lazy بالفعل
        if 'loading=' in attrs:
            return match.group(0)
        
        # تخطي صور hero carousel الأولى
        if 'carousel-item active' in content[max(0, match.start()-200):match.start()]:
            return match.group(0)
        
        # إضافة loading="lazy"
        if attrs.strip():
            return f'<img src="assets/img/{src}"{attrs} loading="lazy">'
        else:
            return f'<img src="assets/img/{src}" loading="lazy">'
    
    new_content = re.sub(img_pattern, add_lazy, content)
    if new_content != content:
        content = new_content
        changes.append("✓ Added lazy loading")
    
    # 5. تحويل صور الفريق إلى WebP
    team_pattern = r'<img src="assets/img/team/(team-\d+\.jpg)" class="img-fluid" alt="([^"]*)"([^>]*)>'
    
    def convert_team(match):
        img_file = match.group(1)
        alt = match.group(2)
        attrs = match.group(3)
        webp_file = img_file.replace('.jpg', '.webp')
        
        return f'''<picture>
                <source srcset="assets/img/team/{webp_file}" type="image/webp">
                <img src="assets/img/team/{img_file}" class="img-fluid" alt="{alt}"{attrs}>
              </picture>'''
    
    new_content = re.sub(team_pattern, convert_team, content)
    if new_content != content:
        content = new_content
        changes.append("✓ Team images → WebP")
    
    # 6. تحويل صور المقالات والخلفيات
    constructions_pattern = r'<img src="assets/img/(constructions-\d+\.jpg)"([^>]*)>'
    
    def convert_constructions(match):
        img_file = match.group(1)
        attrs = match.group(2)
        webp_file = img_file.replace('.jpg', '.webp')
        
        return f'''<picture>
              <source srcset="assets/img/{webp_file}" type="image/webp">
              <img src="assets/img/{img_file}"{attrs}>
            </picture>'''
    
    new_content = re.sub(constructions_pattern, convert_constructions, content)
    if new_content != content:
        content = new_content
        changes.append("✓ Article images → WebP")
    
    # حفظ التغييرات
    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("\n📝 Changes made:")
        for change in changes:
            print(f"   {change}")
        print(f"\n✅ File updated successfully!")
        return True
    else:
        print("\n⊘ No changes needed")
        return False

# تشغيل التحسين
print("\n" + "="*60)
print("🚀 STARTING WEBSITE OPTIMIZATION")
print("="*60)

updated = 0
skipped = 0

for html_file in html_files:
    file_path = base_dir / html_file
    if optimize_page(file_path):
        updated += 1
    else:
        skipped += 1

print("\n" + "="*60)
print("📊 OPTIMIZATION SUMMARY")
print("="*60)
print(f"✅ Updated: {updated} files")
print(f"⊘ Skipped: {skipped} files")
print(f"📁 Total: {len(html_files)} files")
print("="*60)
print("\n✨ Optimization complete!")
