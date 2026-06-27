@echo off
chcp 65001 >nul
REM ============================================================
REM  vision-skill Windows 离线依赖一键安装脚本
REM ============================================================
setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "COMMON_DIR=%SCRIPT_DIR%common"
set "WIN_DIR=%SCRIPT_DIR%windows"
set "REQUIREMENTS=%SCRIPT_DIR%..\requirements.txt"

echo.
echo ============================================
echo   vision-skill Windows 离线依赖安装
echo ============================================
echo.

REM 检查 Python
set "PYTHON="
for %%p in (python python3) do (
    where %%p >nul 2>&1
    if !errorlevel! equ 0 (
        for /f "tokens=2 delims= " %%v in ('%%p --version 2^>^&1') do (
            set "ver=%%v"
            for /f "tokens=1,2 delims=." %%a in ("!ver!") do (
                set "major=%%a"
                set "minor=%%b"
                if !major! geq 3 if !minor! geq 10 (
                    set "PYTHON=%%p"
                )
            )
        )
    )
)

if "%PYTHON%"=="" (
    echo [ERROR] 未找到 Python 3.10+，请先安装 Python
    echo         下载: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [INFO] 使用 Python:
%PYTHON% --version

REM 检查离线包目录
if not exist "%COMMON_DIR%" (
    echo [ERROR] 离线包目录不存在: %COMMON_DIR%
    pause
    exit /b 1
)
if not exist "%WIN_DIR%" (
    echo [ERROR] 离线包目录不存在: %WIN_DIR%
    pause
    exit /b 1
)

REM 检查 requirements.txt
if not exist "%REQUIREMENTS%" (
    echo [ERROR] requirements.txt 不存在: %REQUIREMENTS%
    pause
    exit /b 1
)

REM 统计离线包
set "common_count=0"
for %%f in ("%COMMON_DIR%\*.whl" "%COMMON_DIR%\*.tar.gz") do set /a common_count+=1 2>nul
set "win_count=0"
for %%f in ("%WIN_DIR%\*.whl" "%WIN_DIR%\*.tar.gz") do set /a win_count+=1 2>nul
echo [INFO] 离线包: common %common_count% 个 + windows %win_count% 个

REM 检查 crcmod 是否需要编译
echo.
echo [INFO] 注意: crcmod 为源码包，需要 C++ 编译器
echo       如安装失败，请安装 Microsoft C++ Build Tools:
echo       https://visualstudio.microsoft.com/visual-cpp-build-tools/
echo.

REM 安装
echo [INFO] 开始离线安装...
echo.

%PYTHON% -m pip install --no-index ^
    --find-links "%COMMON_DIR%" ^
    --find-links "%WIN_DIR%" ^
    -r "%REQUIREMENTS%"

if %errorlevel% neq 0 (
    echo.
    echo ============================================
    echo [WARN] 安装遇到问题，尝试单独安装 crcmod...
    echo ============================================
    echo.

    REM 先装其他依赖
    %PYTHON% -m pip install --no-index ^
        --find-links "%COMMON_DIR%" ^
        --find-links "%WIN_DIR%" ^
        requests python-dotenv cos-python-sdk-v5

    REM 单独装 crcmod
    echo.
    echo [INFO] 尝试编译安装 crcmod...
    %PYTHON% -m pip install --no-index --find-links "%COMMON_DIR%" crcmod

    if !errorlevel! neq 0 (
        echo.
        echo ============================================
        echo [ERROR] crcmod 编译失败
        echo ============================================
        echo crcmod 需要 Microsoft C++ Build Tools 才能编译。
        echo 请安装后重试:
        echo   https://visualstudio.microsoft.com/visual-cpp-build-tools/
        echo.
        echo 安装时请勾选 "C++ build tools" 工作负载。
        echo.
        pause
        exit /b 1
    )
)

echo.
echo [OK] 安装完成!

REM 验证
echo.
echo [INFO] 验证已安装的包:
echo   (可使用以下命令手动验证各包导入)
echo     %PYTHON% -c "import requests, dotenv, charset_normalizer, urllib3, certifi, idna, xmltodict, six, crcmod; from qcloud_cos import CosS3Client; import Crypto; print('OK')"

echo.
echo ============================================
echo   所有依赖已就绪!
echo ============================================

REM 不自动关闭窗口
pause
