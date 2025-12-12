@echo off
REM Quick Start Deployment Script for Windows
REM This script helps you prepare for deployment

echo.
echo 🚀 GETNOTIFY Deployment Preparation
echo ====================================
echo.

REM Check if .env exists
if not exist .env (
    echo ⚠️  .env file not found!
    echo Creating .env template...
    (
        echo # Supabase Configuration
        echo SUPABASE_URL=https://hfsazlirxtjbarftyoqh.supabase.co
        echo SUPABASE_KEY=your-service-role-key-here
        echo.
        echo # SendGrid (Optional - for email notifications)
        echo SENDGRID_API_KEY=your-sendgrid-api-key-here
    ) > .env
    echo ✅ Created .env template. Please fill in your values!
) else (
    echo ✅ .env file exists
)

echo.
echo Checking dependencies...
findstr /C:"supabase" requirements.txt >nul && findstr /C:"undetected-chromedriver" requirements.txt >nul
if %errorlevel% equ 0 (
    echo ✅ All required dependencies are in requirements.txt
) else (
    echo ⚠️  Some dependencies might be missing
)

echo.
echo Checking Dockerfile...
if exist dockerfile (
    echo ✅ Dockerfile exists
) else (
    echo ⚠️  Dockerfile not found
)

echo.
echo 📋 Deployment Checklist:
echo   [ ] Code pushed to GitHub
echo   [ ] Environment variables configured in deployment platform
echo   [ ] Supabase redirect URLs updated
echo   [ ] Google OAuth redirect URLs updated
echo   [ ] Frontend API URL configured (via meta tag or app.js)
echo.
echo 📖 Read DEPLOYMENT_GUIDE.md for detailed instructions
echo.
echo ✨ Ready to deploy!
pause
