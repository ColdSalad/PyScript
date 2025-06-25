@echo off
chcp 65001 >nul
echo ====================================
echo    Instagram登录GUI打包工具
echo ====================================
echo.

echo 正在执行打包...
python build_exe.py

echo.
echo 打包完成！
echo 请查看 dist 文件夹中的 InstagramLogin.exe
echo.
pause 