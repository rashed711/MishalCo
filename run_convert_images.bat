@echo off
echo ========================================
echo تحديث مراجع الصور إلى WebP
echo ========================================
echo.
echo هذا السكربت سيقوم بتحديث جميع مراجع الصور
echo في ملفات HTML من JPG/PNG إلى WebP
echo.
pause
echo.
python convert_images_to_webp.py
echo.
echo ========================================
echo تم الانتهاء!
echo ========================================
echo.
pause
