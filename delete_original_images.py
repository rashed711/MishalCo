import os

# المسار إلى مجلد الصور
base_dir = r"d:\Programs\Androide\websites\MishalCo\assets\img"
extensions = ('.jpg', '.jpeg', '.png')

def delete_original_images(root_dir):
    print(f"Starting deletion of original images in: {root_dir}")
    deleted_count = 0
    total_space_saved = 0
    
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(extensions):
                file_path = os.path.join(root, file)
                file_name, _ = os.path.splitext(file)
                webp_path = os.path.join(root, file_name + ".webp")
                
                # حذف الملف الأصلي فقط إذا كان ملف WebP موجوداً
                if os.path.exists(webp_path):
                    try:
                        file_size = os.path.getsize(file_path)
                        os.remove(file_path)
                        deleted_count += 1
                        total_space_saved += file_size
                        print(f"✓ Deleted: {file} (Size: {file_size / 1024:.2f} KB)")
                    except Exception as e:
                        print(f"✗ Error deleting {file}: {e}")
                else:
                    print(f"⊘ Skipped: {file} (No WebP version found)")
    
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"Total files deleted: {deleted_count}")
    print(f"Total space saved: {total_space_saved / (1024 * 1024):.2f} MB")
    print(f"{'='*60}")

if __name__ == "__main__":
    # تأكيد من المستخدم قبل الحذف
    print("⚠️  WARNING: This will delete all original JPG/PNG images that have WebP versions!")
    print(f"Directory: {base_dir}")
    
    response = input("\nAre you sure you want to continue? (yes/no): ")
    
    if response.lower() in ['yes', 'y', 'نعم']:
        delete_original_images(base_dir)
    else:
        print("Operation cancelled.")
