@echo off
echo ========================================
echo تشغيل سكربت حذف الصور الأصلية
echo ========================================
echo.
echo هذا السكربت سيحذف جميع الصور الأصلية (JPG/PNG)
echo التي تم تحويلها إلى WebP
echo.
echo تأكد من وجود نسخة احتياطية قبل المتابعة!
echo.
pause
echo.
python delete_original_images.py
echo.
pause
