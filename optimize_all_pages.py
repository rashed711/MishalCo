import os
import re

# قائمة الصفحات المراد تحديثها
pages = [
    'contact.html',
    'book_consultation.html',
    'Complaints.html',
    'FAQ.html',
    'blog.html',
    'projects.html',
    'photosss.html',
    '404.html'
]

base_dir = r"d:\Programs\Androide\websites\MishalCo"

def optimize_html_file(file_path):
    """تحسين ملف HTML واحد"""
    if not os.path.exists(file_path):
        print(f"⊘ File not found: {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes_made = []
    
    # 1. تحويل الشعار إلى WebP
    logo_pattern = r'<img\s+src="assets/img/logo\.png"\s+alt="([^"]*)">'
    logo_replacement = r'''<picture>
          <source srcset="assets/img/logo.webp" type="image/webp">
          <img src="assets/img/logo.png" alt="\1">
        </picture>'''
    if re.search(logo_pattern, content):
        content = re.sub(logo_pattern, logo_replacement, content)
        changes_made.append("Logo converted to WebP")
    
    # 2. إضافة defer للسكربتات
    script_patterns = [
        (r'<script\s+src="([^"]*bootstrap[^"]*\.js)">', r'<script src="\1" defer>'),
        (r'<script\s+src="([^"]*aos[^"]*\.js)">', r'<script src="\1" defer>'),
        (r'<script\s+src="([^"]*glightbox[^"]*\.js)">', r'<script src="\1" defer>'),
        (r'<script\s+src="([^"]*purecounter[^"]*\.js)">', r'<script src="\1" defer>'),
        (r'<script\s+src="([^"]*swiper[^"]*\.js)">', r'<script src="\1" defer>'),
        (r'<script\s+src="([^"]*jquery[^"]*\.js)">', r'<script src="\1" defer>'),
        (r'<script\s+src="([^"]*isotope[^"]*\.js)">', r'<script src="\1" defer>'),
        (r'<script\s+src="([^"]*imagesloaded[^"]*\.js)">', r'<script src="\1" defer>'),
        (r'<script\s+src="assets/js/main\.js">', r'<script src="assets/js/main.js" defer>'),
    ]
    
    for pattern, replacement in script_patterns:
        if re.search(pattern, content) and 'defer' not in content:
            content = re.sub(pattern, replacement, content)
            changes_made.append("Added defer to scripts")
            break
    
    # 3. تحويل صورة الواتساب إلى WebP
    whatsapp_pattern = r'<img\s+src="assets/img/whatsapp\.png"\s+alt="([^"]*)"\s+class="whatsapp-icon"([^>]*)>'
    whatsapp_replacement = r'''<picture>
      <source srcset="assets/img/whatsapp.webp" type="image/webp">
      <img src="assets/img/whatsapp.png" alt="\1" class="whatsapp-icon"\2>
    </picture>'''
    if re.search(whatsapp_pattern, content):
        content = re.sub(whatsapp_pattern, whatsapp_replacement, content)
        changes_made.append("WhatsApp image converted to WebP")
    
    # 4. إضافة loading="lazy" للصور (ما عدا الصور الأولى)
    # نبحث عن صور بدون loading attribute
    img_pattern = r'<img\s+(?![^>]*loading=)([^>]*src="assets/img/[^"]*\.(jpg|png)"[^>]*)>'
    def add_lazy_loading(match):
        img_tag = match.group(0)
        # لا نضيف lazy للصور في الـ hero section أو الصور الأولى
        if 'hero-carousel' in img_tag or 'carousel-item active' in img_tag:
            return img_tag
        # إضافة loading="lazy" قبل >
        return img_tag.replace('>', ' loading="lazy">')
    
    content = re.sub(img_pattern, add_lazy_loading, content)
    
    # 5. تحويل صور الفريق إلى WebP
    team_img_pattern = r'<img\s+src="assets/img/team/([^"]+\.jpg)"\s+class="img-fluid"\s+alt="([^"]*)"([^>]*)>'
    def convert_team_img(match):
        img_name = match.group(1)
        alt_text = match.group(2)
        extra_attrs = match.group(3)
        webp_name = img_name.replace('.jpg', '.webp')
        return f'''<picture>
                <source srcset="assets/img/team/{webp_name}" type="image/webp">
                <img src="assets/img/team/{img_name}" class="img-fluid" alt="{alt_text}"{extra_attrs}>
              </picture>'''
    
    content = re.sub(team_img_pattern, convert_team_img, content)
    
    # حفظ الملف إذا تم إجراء تغييرات
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Updated: {os.path.basename(file_path)}")
        for change in set(changes_made):
            print(f"  - {change}")
        return True
    else:
        print(f"⊘ No changes needed: {os.path.basename(file_path)}")
        return False

# تشغيل التحسين على جميع الصفحات
print("="*60)
print("Starting HTML optimization for all pages...")
print("="*60)
print()

updated_count = 0
for page in pages:
    file_path = os.path.join(base_dir, page)
    if optimize_html_file(file_path):
        updated_count += 1
    print()

print("="*60)
print(f"Summary: {updated_count} files updated out of {len(pages)}")
print("="*60)
