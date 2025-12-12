"""
سكربت لإنشاء نسخ مصغرة من صور Hero للموبايل
هذا سيحسن LCP على الموبايل بشكل كبير
"""

from PIL import Image
import os

# المجلد الأساسي
base_dir = r"d:\Programs\Androide\websites\MishalCo\assets\img\hero-carousel"

# أحجام مختلفة للموبايل
sizes = {
    'mobile': (768, 432),    # للموبايل
    'tablet': (1024, 576),   # للتابلت
    # الحجم الأصلي 1920x1080 للكمبيوتر
}

# قائمة الصور
images = [
    'hero-carousel-1.webp',
    'hero-carousel-2.webp',
    'hero-carousel-3.webp',
    'hero-carousel-4.webp',
    'hero-carousel-5.webp'
]

print("="*60)
print("🖼️  إنشاء نسخ مصغرة للصور - Responsive Images")
print("="*60)
print()

total_saved = 0

for img_name in images:
    img_path = os.path.join(base_dir, img_name)
    
    if not os.path.exists(img_path):
        print(f"⊘ {img_name} - not found")
        continue
    
    try:
        # فتح الصورة
        img = Image.open(img_path)
        original_size = os.path.getsize(img_path)
        
        print(f"📸 {img_name}")
        print(f"   Original: {img.size[0]}x{img.size[1]} ({original_size/1024:.1f} KB)")
        
        # إنشاء نسخ مصغرة
        for size_name, (width, height) in sizes.items():
            # اسم الملف الجديد
            base_name = img_name.replace('.webp', '')
            new_name = f"{base_name}-{size_name}.webp"
            new_path = os.path.join(base_dir, new_name)
            
            # تصغير الصورة
            resized = img.copy()
            resized.thumbnail((width, height), Image.Resampling.LANCZOS)
            
            # حفظ بجودة 80%
            resized.save(new_path, 'WEBP', quality=80, method=6)
            
            new_size = os.path.getsize(new_path)
            saved = original_size - new_size
            total_saved += saved
            
            print(f"   ✓ {size_name}: {resized.size[0]}x{resized.size[1]} ({new_size/1024:.1f} KB) - saved {saved/1024:.1f} KB")
        
        print()
        
    except Exception as e:
        print(f"❌ Error: {img_name} - {e}")
        print()

print("="*60)
print(f"✅ Total space saved: {total_saved/1024/1024:.2f} MB")
print("="*60)
print()
print("🎯 Next steps:")
print("   1. Update index.html to use responsive images")
print("   2. Test on mobile devices")
print("   3. Re-test on Google PageSpeed")
print("="*60)
