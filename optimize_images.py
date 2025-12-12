import os
from PIL import Image

# المسار إلى مجلد الصور
base_dir = r"d:\Programs\Androide\websites\MishalCo\assets\img"
extensions = ('.jpg', '.jpeg', '.png')

def convert_to_webp(root_dir):
    print(f"Starting optimization in: {root_dir}")
    
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(extensions):
                file_path = os.path.join(root, file)
                file_name, _ = os.path.splitext(file)
                webp_path = os.path.join(root, file_name + ".webp")
                
                # تخطي الملف إذا كان موجوداً مسبقاً
                if os.path.exists(webp_path):
                    continue
                
                try:
                    with Image.open(file_path) as img:
                        # تحويل الصورة إلى RGB إذا كانت بوضع RGBA (في حال كانت PNG)
                        if img.mode in ("RGBA", "P"):
                            img = img.convert("RGB")
                        
                        # حفظ الصورة بصيغة WebP مع جودة 80%
                        img.save(webp_path, "WEBP", quality=80)
                        
                        original_size = os.path.getsize(file_path)
                        new_size = os.path.getsize(webp_path)
                        savings = original_size - new_size
                        
                        print(f"Converted: {file} -> {os.path.basename(webp_path)} | Saved: {savings / 1024:.2f} KB")

                        # حذف الملف الأصلي بعد التحويل الناجح
                        os.remove(file_path)
                        print(f"Deleted original file: {file}")
                        
                except Exception as e:
                    print(f"Error converting {file}: {e}")

if __name__ == "__main__":
    convert_to_webp(base_dir)
